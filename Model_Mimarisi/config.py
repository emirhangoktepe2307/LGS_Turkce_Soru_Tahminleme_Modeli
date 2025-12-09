"""
LGS Türkçe Soru Üretici - Yapılandırma Dosyası
Bu dosya API anahtarlarını ve sistem ayarlarını içerir.
"""

import os
from pathlib import Path

# ==================== API AYARLARI ====================
# Gemini API anahtarınızı buraya girin veya çevre değişkeni olarak ayarlayın
# Google AI Studio'dan ücretsiz API anahtarı alabilirsiniz: https://makersuite.google.com/app/apikey
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "BURAYA_API_ANAHTARINIZI_GIRIN")

# ==================== VERİTABANI AYARLARI ====================
# ChromaDB veritabanı dizini
BASE_DIR = Path(__file__).parent
CHROMA_PERSIST_DIR = str(BASE_DIR / "chroma_db")
COLLECTION_NAME = "lgs_turkce_sorulari"

# Veri dosyası yolu
DATA_FILE = str(BASE_DIR / "lgs_turkce_sorulari.json")

# ==================== MODEL AYARLARI ====================
# Gemini model seçimi
GEMINI_MODEL = "gemini-1.5-flash"  # veya "gemini-1.5-pro" daha kapsamlı yanıtlar için

# Embedding model
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # SentenceTransformer modeli

# ==================== SORU ÜRETİM AYARLARI ====================
# Varsayılan zorluk seviyeleri
ZORLUK_SEVIYELERI = ["Kolay", "Orta", "Zor"]

# Türkçe dersi konu başlıkları
TURKCE_KONULARI = [
    "Sözcükte Anlam",
    "Cümlede Anlam",
    "Paragrafta Anlam",
    "Dil Bilgisi",
    "Yazım Kuralları",
    "Noktalama İşaretleri",
    "Söz Sanatları",
    "Anlatım Bozuklukları",
    "Fiilde Çatı",
    "Cümle Türleri"
]

# Alt konu başlıkları
ALT_KONULAR = {
    "Sözcükte Anlam": [
        "Eş Anlamlı Sözcükler",
        "Zıt Anlamlı Sözcükler",
        "Mecaz Anlam",
        "Sesteş Sözcükler",
        "Terim Anlam",
        "Çok Anlamlılık"
    ],
    "Cümlede Anlam": [
        "Öznel ve Nesnel Yargı",
        "Neden-Sonuç İlişkisi",
        "Koşul-Sonuç İlişkisi",
        "Amaç-Sonuç İlişkisi",
        "Karşılaştırma"
    ],
    "Paragrafta Anlam": [
        "Ana Düşünce",
        "Yardımcı Düşünce",
        "Paragrafta Başlık",
        "Paragraf Tamamlama",
        "Paragrafta Anlam Akışı"
    ],
    "Dil Bilgisi": [
        "Fiil Kipleri",
        "İsim Tamlaması",
        "Sıfatlar",
        "Zarflar",
        "Zamirler",
        "Edatlar"
    ],
    "Yazım Kuralları": [
        "Büyük Harflerin Yazımı",
        "Ki'nin Yazımı",
        "De'nin Yazımı",
        "Birleşik Sözcüklerin Yazımı"
    ],
    "Noktalama İşaretleri": [
        "Virgül Kullanımı",
        "İki Nokta Kullanımı",
        "Noktalı Virgül",
        "Tırnak İşareti"
    ],
    "Söz Sanatları": [
        "Benzetme",
        "Kişileştirme",
        "Abartma",
        "Konuşturma"
    ],
    "Anlatım Bozuklukları": [
        "Gereksiz Sözcük Kullanımı",
        "Özne-Yüklem Uyumsuzluğu",
        "Anlam Belirsizliği",
        "Çelişki"
    ],
    "Fiilde Çatı": [
        "Ettirgen Çatı",
        "Edilgen Çatı",
        "Dönüşlü Çatı",
        "İşteş Çatı"
    ],
    "Cümle Türleri": [
        "Yapısına Göre Cümle",
        "Anlamına Göre Cümle",
        "Yüklemine Göre Cümle"
    ]
}

# ==================== SİSTEM MESAJLARI ====================
# Türkçe dışı konular için uyarı mesajı
KONU_DISI_UYARI = """
⚠️ Bu sistem sadece LGS Türkçe dersi soruları için tasarlanmıştır.

Matematik, Fen Bilimleri, Sosyal Bilgiler, Din Kültürü, İngilizce gibi 
diğer derslerle ilgili sorulara yanıt veremiyorum.

Lütfen Türkçe dersiyle ilgili bir soru sorun veya soru üretmemi isteyin.
"""

# Karşılama mesajı
KARSILAMA_MESAJI = """
🎓 LGS Türkçe Soru Üretici'ye Hoş Geldiniz!

Bu sistem, geçmiş yılların LGS Türkçe sorularını analiz ederek 
yeni ve özgün sorular üretmenize yardımcı olur.

📚 Yapabileceklerim:
• Belirli bir konuda yeni soru üretmek
• Mevcut sorulara benzer sorular oluşturmak
• Farklı zorluk seviyelerinde sorular hazırlamak
• Türkçe konularında açıklama yapmak

🔍 Örnek Kullanım:
"Sözcükte anlam konusunda orta zorlukta 3 soru üret"
"Fiilde çatı konusunu açıkla"
"Paragraf sorusu oluştur"
"""

