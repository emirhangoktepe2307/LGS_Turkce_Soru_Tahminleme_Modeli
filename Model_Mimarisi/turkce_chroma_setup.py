"""
LGS Türkçe Soruları - ChromaDB Vektör Veritabanı Kurulumu
Bu dosya, Türkçe sorularını ChromaDB'ye yükler ve semantik arama yapılmasını sağlar.
"""

import json
import chromadb
from chromadb.utils import embedding_functions
from chromadb.config import Settings
from pathlib import Path
from config import CHROMA_PERSIST_DIR, COLLECTION_NAME, DATA_FILE, EMBEDDING_MODEL


def create_chroma_client():
    """Kalıcı ChromaDB istemcisi oluşturur."""
    settings = Settings(
        chroma_db_impl="duckdb+parquet",
        persist_directory=CHROMA_PERSIST_DIR,
        anonymized_telemetry=False
    )
    
    client = chromadb.Client(settings)
    return client


def get_embedding_function():
    """SentenceTransformer embedding fonksiyonunu döndürür."""
    return embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=EMBEDDING_MODEL
    )


def load_questions_from_json(file_path: str) -> dict:
    """JSON dosyasından soruları yükler."""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def setup_collection(client, embedding_function):
    """Koleksiyon oluşturur veya mevcut olanı getirir."""
    try:
        # Mevcut koleksiyonu sil ve yeniden oluştur
        try:
            client.delete_collection(name=COLLECTION_NAME)
            print(f"📦 Mevcut '{COLLECTION_NAME}' koleksiyonu silindi.")
        except:
            pass
        
        collection = client.create_collection(
            name=COLLECTION_NAME,
            embedding_function=embedding_function,
            metadata={"description": "LGS Türkçe Soruları Veritabanı"}
        )
        print(f"✅ '{COLLECTION_NAME}' koleksiyonu oluşturuldu.")
        return collection
    except Exception as e:
        print(f"❌ Koleksiyon oluşturma hatası: {e}")
        raise


def add_questions_to_collection(collection, data: dict):
    """Soruları koleksiyona ekler."""
    sorular = data.get("sorular", [])
    
    if not sorular:
        print("⚠️ Eklenecek soru bulunamadı!")
        return
    
    documents = []
    metadatas = []
    ids = []
    
    for soru in sorular:
        # Soru metnini ve cevabı birleştir (daha iyi embedding için)
        full_text = f"""
        Konu: {soru['konu']} - {soru['alt_konu']}
        Soru: {soru['soru_metni']}
        Doğru Cevap: {soru['dogru_cevap']}
        Açıklama: {soru['cevap_aciklamasi']}
        """
        
        documents.append(full_text)
        
        metadatas.append({
            "id": soru["id"],
            "yil": soru["yil"],
            "konu": soru["konu"],
            "alt_konu": soru["alt_konu"],
            "zorluk": soru["zorluk"],
            "dogru_cevap": soru["dogru_cevap"],
            "anahtar_kelimeler": ", ".join(soru["anahtar_kelimeler"])
        })
        
        ids.append(soru["id"])
    
    # Toplu ekleme
    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    
    print(f"✅ {len(sorular)} soru başarıyla veritabanına eklendi.")


def query_similar_questions(collection, query_text: str, n_results: int = 5, 
                           konu_filtresi: str = None):
    """Benzer soruları sorgular."""
    where_filter = None
    if konu_filtresi:
        where_filter = {"konu": konu_filtresi}
    
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results,
        where=where_filter
    )
    
    return results


def get_questions_by_topic(collection, konu: str, n_results: int = 10):
    """Belirli bir konudaki soruları getirir."""
    results = collection.query(
        query_texts=[konu],
        n_results=n_results,
        where={"konu": konu}
    )
    return results


def get_collection_stats(collection):
    """Koleksiyon istatistiklerini döndürür."""
    count = collection.count()
    return {
        "toplam_soru": count,
        "koleksiyon_adi": COLLECTION_NAME
    }


def initialize_database():
    """Veritabanını başlatır ve soruları yükler."""
    print("🚀 LGS Türkçe Soru Veritabanı Kurulumu Başlatılıyor...")
    print("-" * 50)
    
    # ChromaDB istemcisi oluştur
    client = create_chroma_client()
    print("✅ ChromaDB istemcisi oluşturuldu.")
    
    # Embedding fonksiyonu
    embedding_function = get_embedding_function()
    print(f"✅ Embedding modeli yüklendi: {EMBEDDING_MODEL}")
    
    # Koleksiyon oluştur
    collection = setup_collection(client, embedding_function)
    
    # Soruları JSON'dan yükle
    if Path(DATA_FILE).exists():
        data = load_questions_from_json(DATA_FILE)
        print(f"✅ Veri dosyası yüklendi: {DATA_FILE}")
        
        # Soruları ekle
        add_questions_to_collection(collection, data)
    else:
        print(f"⚠️ Veri dosyası bulunamadı: {DATA_FILE}")
    
    # İstatistikleri göster
    stats = get_collection_stats(collection)
    print("-" * 50)
    print(f"📊 Veritabanı İstatistikleri:")
    print(f"   Toplam Soru: {stats['toplam_soru']}")
    print(f"   Koleksiyon: {stats['koleksiyon_adi']}")
    
    return client, collection


def test_query(collection):
    """Test sorgusu yapar."""
    print("\n🔍 Test Sorgusu Yapılıyor...")
    print("-" * 50)
    
    test_queries = [
        "Eş anlamlı sözcükler nedir?",
        "Fiilde çatı konusu",
        "Paragrafta ana düşünce nasıl bulunur?"
    ]
    
    for query in test_queries:
        print(f"\n📝 Sorgu: {query}")
        results = query_similar_questions(collection, query, n_results=2)
        
        if results['documents'][0]:
            for i, (doc, metadata) in enumerate(zip(results['documents'][0], results['metadatas'][0])):
                print(f"\n   Sonuç {i+1}:")
                print(f"   Konu: {metadata['konu']} - {metadata['alt_konu']}")
                print(f"   Zorluk: {metadata['zorluk']}")


if __name__ == "__main__":
    # Veritabanını başlat
    client, collection = initialize_database()
    
    # Test sorgusu yap
    test_query(collection)
    
    print("\n✅ Kurulum tamamlandı!")

