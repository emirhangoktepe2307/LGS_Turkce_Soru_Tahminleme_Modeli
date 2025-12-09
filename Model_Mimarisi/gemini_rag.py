"""
LGS Türkçe RAG Sistemi - Gemini API Entegrasyonu
Bu dosya, Gemini API kullanarak RAG (Retrieval-Augmented Generation) sistemi sağlar.
"""

import google.generativeai as genai
from typing import List, Dict, Optional
import json
import re
from config import (
    GEMINI_API_KEY, 
    GEMINI_MODEL, 
    TURKCE_KONULARI,
    ALT_KONULAR,
    KONU_DISI_UYARI,
    ZORLUK_SEVIYELERI
)


class TurkceRAG:
    """LGS Türkçe soruları için RAG sistemi."""
    
    def __init__(self, collection=None):
        """RAG sistemini başlatır."""
        self.collection = collection
        self._setup_gemini()
        self._create_system_prompt()
    
    def _setup_gemini(self):
        """Gemini API'yi yapılandırır."""
        if GEMINI_API_KEY == "BURAYA_API_ANAHTARINIZI_GIRIN":
            raise ValueError(
                "Lütfen config.py dosyasında GEMINI_API_KEY değerini ayarlayın!\n"
                "API anahtarı almak için: https://makersuite.google.com/app/apikey"
            )
        
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(GEMINI_MODEL)
        print(f"✅ Gemini modeli yüklendi: {GEMINI_MODEL}")
    
    def _create_system_prompt(self):
        """Sistem promptunu oluşturur."""
        self.system_prompt = """
Sen bir LGS (Liselere Geçiş Sınavı) Türkçe dersi uzmanısın. 
Görevin, öğrencilere Türkçe dersi konularında yardımcı olmak ve 
geçmiş yılların LGS sorularına benzer yeni sorular üretmektir.

ÖNEMLİ KURALLAR:
1. SADECE Türkçe dersiyle ilgili sorulara cevap ver.
2. Matematik, Fen Bilimleri, Sosyal Bilgiler, Din Kültürü, İngilizce 
   gibi diğer derslerle ilgili sorulara ASLA cevap verme.
3. Konu dışı sorularda kibarca uyar ve Türkçe konularına yönlendir.
4. Ürettiğin sorular LGS formatına uygun olmalı (4 seçenekli, A-B-C-D).
5. Her sorunun açıklamalı cevabını da sun.
6. Türkçe dil bilgisi kurallarına uygun, anlaşılır sorular üret.

TÜRKÇE DERSİ KONULARI:
- Sözcükte Anlam (eş anlam, zıt anlam, mecaz anlam, sesteş sözcükler)
- Cümlede Anlam (öznel/nesnel yargı, neden-sonuç, koşul-sonuç)
- Paragrafta Anlam (ana düşünce, yardımcı düşünce, başlık)
- Dil Bilgisi (fiil kipleri, isim tamlaması, sıfatlar, zarflar)
- Yazım Kuralları (büyük harf, ki/de yazımı)
- Noktalama İşaretleri (virgül, iki nokta, noktalı virgül)
- Söz Sanatları (benzetme, kişileştirme, abartma)
- Anlatım Bozuklukları (gereksiz sözcük, özne-yüklem uyumu)
- Fiilde Çatı (ettirgen, edilgen, dönüşlü, işteş)
- Cümle Türleri (basit, birleşik, sıralı)
"""
    
    def is_turkce_related(self, query: str) -> bool:
        """Sorgunun Türkçe dersiyle ilgili olup olmadığını kontrol eder."""
        # Türkçe ile ilgili anahtar kelimeler
        turkce_keywords = [
            "türkçe", "sözcük", "cümle", "paragraf", "anlam", "dil bilgisi",
            "yazım", "noktalama", "söz sanatı", "anlatım", "fiil", "isim",
            "sıfat", "zarf", "zamir", "edat", "bağlaç", "ünlem", "kip",
            "çatı", "tamlama", "özne", "yüklem", "nesne", "tümleç",
            "eş anlam", "zıt anlam", "mecaz", "benzetme", "kişileştirme",
            "virgül", "nokta", "soru", "üret", "oluştur", "hazırla",
            "lgs", "sınav", "test", "kolay", "orta", "zor"
        ]
        
        # Diğer derslerle ilgili anahtar kelimeler
        diger_dersler = [
            "matematik", "toplama", "çıkarma", "çarpma", "bölme", "denklem",
            "geometri", "üçgen", "kare", "daire", "alan", "çevre", "hacim",
            "fen", "fizik", "kimya", "biyoloji", "hücre", "atom", "molekül",
            "enerji", "kuvvet", "hareket", "ısı", "elektrik", "mıknatıs",
            "sosyal", "tarih", "coğrafya", "vatandaşlık", "inkılap", "atatürk",
            "ingilizce", "english", "grammar", "vocabulary", "reading",
            "din", "ibadet", "namaz", "oruç", "zekat", "hac"
        ]
        
        query_lower = query.lower()
        
        # Diğer derslerle ilgili mi kontrol et
        for keyword in diger_dersler:
            if keyword in query_lower:
                return False
        
        # Türkçe ile ilgili mi kontrol et (en az bir anahtar kelime varsa veya genel soru ise)
        for keyword in turkce_keywords:
            if keyword in query_lower:
                return True
        
        # Eğer hiçbir anahtar kelime yoksa, Gemini'ye sor
        return True  # Varsayılan olarak kabul et, Gemini kontrol edecek
    
    def get_relevant_context(self, query: str, n_results: int = 5) -> str:
        """Veritabanından ilgili bağlamı getirir."""
        if self.collection is None:
            return ""
        
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            if not results['documents'][0]:
                return ""
            
            context_parts = []
            for doc, metadata in zip(results['documents'][0], results['metadatas'][0]):
                context_parts.append(f"""
---
Konu: {metadata['konu']} - {metadata['alt_konu']}
Zorluk: {metadata['zorluk']}
Yıl: {metadata['yil']}
{doc}
---
""")
            
            return "\n".join(context_parts)
        
        except Exception as e:
            print(f"⚠️ Bağlam getirme hatası: {e}")
            return ""
    
    def generate_response(self, user_query: str) -> str:
        """Kullanıcı sorgusuna yanıt üretir."""
        # Türkçe ile ilgili mi kontrol et
        if not self.is_turkce_related(user_query):
            return KONU_DISI_UYARI
        
        # Veritabanından ilgili bağlamı getir
        context = self.get_relevant_context(user_query)
        
        # Prompt oluştur
        if context:
            prompt = f"""
{self.system_prompt}

REFERANS SORULAR (Veritabanından):
{context}

KULLANICI İSTEĞİ:
{user_query}

Yukarıdaki referans sorulara benzer tarzda, LGS formatına uygun yanıt ver.
Eğer soru üretilmesi isteniyorsa, 4 seçenekli (A-B-C-D) sorular üret ve 
her sorunun doğru cevabını ve açıklamasını da ekle.
"""
        else:
            prompt = f"""
{self.system_prompt}

KULLANICI İSTEĞİ:
{user_query}

LGS formatına uygun yanıt ver. Eğer soru üretilmesi isteniyorsa, 
4 seçenekli (A-B-C-D) sorular üret ve her sorunun doğru cevabını 
ve açıklamasını da ekle.
"""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"❌ Yanıt üretilirken bir hata oluştu: {str(e)}"
    
    def generate_questions(self, konu: str, alt_konu: str = None, 
                          zorluk: str = "Orta", adet: int = 3) -> str:
        """Belirli bir konuda soru üretir."""
        # Konu kontrolü
        if konu not in TURKCE_KONULARI:
            return f"❌ Geçersiz konu. Geçerli konular: {', '.join(TURKCE_KONULARI)}"
        
        # Zorluk kontrolü
        if zorluk not in ZORLUK_SEVIYELERI:
            zorluk = "Orta"
        
        # Veritabanından örnek sorular getir
        context = ""
        if self.collection:
            try:
                results = self.collection.query(
                    query_texts=[f"{konu} {alt_konu or ''}"],
                    n_results=5,
                    where={"konu": konu}
                )
                
                if results['documents'][0]:
                    context = "ÖRNEK SORULAR:\n"
                    for doc in results['documents'][0]:
                        context += doc + "\n---\n"
            except:
                pass
        
        prompt = f"""
{self.system_prompt}

{context}

GÖREV:
{konu} konusunda{f' ({alt_konu} alt konusunda)' if alt_konu else ''} 
{zorluk} zorluk seviyesinde {adet} adet LGS formatında soru üret.

FORMAT:
Her soru için:
1. Soru metni (4 seçenekli: A, B, C, D)
2. Doğru cevap
3. Cevap açıklaması

Soruları numaralandır ve açık bir şekilde formatla.
"""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"❌ Soru üretilirken bir hata oluştu: {str(e)}"
    
    def explain_topic(self, konu: str) -> str:
        """Bir konuyu açıklar."""
        if not self.is_turkce_related(konu):
            return KONU_DISI_UYARI
        
        prompt = f"""
{self.system_prompt}

GÖREV:
"{konu}" konusunu LGS'ye hazırlanan 8. sınıf öğrencilerine uygun şekilde açıkla.

AÇIKLAMA İÇERİĞİ:
1. Konunun tanımı
2. Temel kurallar ve özellikler
3. Örnekler
4. LGS'de sık çıkan soru tipleri
5. Dikkat edilmesi gereken noktalar

Açık, anlaşılır ve öğretici bir dil kullan.
"""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"❌ Açıklama üretilirken bir hata oluştu: {str(e)}"


def main():
    """Test fonksiyonu."""
    print("🚀 LGS Türkçe RAG Sistemi Test Ediliyor...")
    print("-" * 50)
    
    try:
        # RAG sistemini başlat (veritabanı olmadan)
        rag = TurkceRAG()
        
        # Test sorguları
        test_queries = [
            "Sözcükte anlam konusunda 2 soru üret",
            "Matematik problemleri çöz",  # Reddedilmeli
            "Fiilde çatı konusunu açıkla"
        ]
        
        for query in test_queries:
            print(f"\n📝 Sorgu: {query}")
            print("-" * 30)
            response = rag.generate_response(query)
            print(response[:500] + "..." if len(response) > 500 else response)
            print("-" * 50)
    
    except ValueError as e:
        print(f"⚠️ {e}")


if __name__ == "__main__":
    main()

