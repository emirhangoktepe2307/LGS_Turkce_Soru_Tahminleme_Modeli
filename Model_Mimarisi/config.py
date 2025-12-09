"""
LGS Türkçe Soru Tahminleme Modeli - Yapılandırma Dosyası
LLM tabanlı soru üretim ve tahminleme sistemi
"""

import os
from pathlib import Path

# ==================== TEMEL AYARLAR ====================
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
MODEL_DIR = BASE_DIR / "models"

# Dizinleri oluştur
DATA_DIR.mkdir(exist_ok=True)
MODEL_DIR.mkdir(exist_ok=True)

# ==================== API AYARLARI ====================
# Gemini API anahtarı (fine-tuning ve inference için)
# API anahtarı almak için: https://makersuite.google.com/app/apikey
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "BURAYA_API_ANAHTARINIZI_GIRIN")

# ==================== MODEL AYARLARI ====================
# Gemini model seçimi
GEMINI_MODEL = "gemini-1.5-flash"  # veya "gemini-1.5-pro"

# Eğitim ayarları
TRAINING_CONFIG = {
    "epochs": 3,
    "batch_size": 8,
    "learning_rate": 2e-5,
    "max_length": 512,
    "train_split": 0.8,
    "validation_split": 0.1,
    "test_split": 0.1
}

# ==================== VERİ DOSYALARI ====================
# Eğitim verisi
TRAINING_DATA_FILE = str(DATA_DIR / "lgs_turkce_egitim_verisi.json")
# Ana soru veritabanı
QUESTIONS_DATA_FILE = str(BASE_DIR / "lgs_turkce_sorulari.json")
# Üretilen sorular
GENERATED_QUESTIONS_FILE = str(DATA_DIR / "uretilen_sorular.json")

# ==================== TÜRKÇE DERSİ KONULARI ====================
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
        "Eş Anlamlı Sözcükler", "Zıt Anlamlı Sözcükler", "Mecaz Anlam",
        "Sesteş Sözcükler", "Terim Anlam", "Çok Anlamlılık", "Deyimler", "Atasözleri"
    ],
    "Cümlede Anlam": [
        "Öznel ve Nesnel Yargı", "Neden-Sonuç İlişkisi", "Koşul-Sonuç İlişkisi",
        "Amaç-Sonuç İlişkisi", "Karşılaştırma"
    ],
    "Paragrafta Anlam": [
        "Ana Düşünce", "Yardımcı Düşünce", "Paragrafta Başlık",
        "Paragraf Tamamlama", "Paragrafta Anlam Akışı"
    ],
    "Dil Bilgisi": [
        "Fiil Kipleri", "İsim Tamlaması", "Sıfatlar", "Zarflar",
        "Zamirler", "Edatlar", "Bağlaçlar"
    ],
    "Yazım Kuralları": [
        "Büyük Harflerin Yazımı", "Ki'nin Yazımı", "De'nin Yazımı",
        "Birleşik Sözcüklerin Yazımı"
    ],
    "Noktalama İşaretleri": [
        "Virgül Kullanımı", "İki Nokta Kullanımı", "Noktalı Virgül", "Tırnak İşareti"
    ],
    "Söz Sanatları": [
        "Benzetme", "Kişileştirme", "Abartma", "Konuşturma"
    ],
    "Anlatım Bozuklukları": [
        "Gereksiz Sözcük Kullanımı", "Özne-Yüklem Uyumsuzluğu",
        "Anlam Belirsizliği", "Çelişki"
    ],
    "Fiilde Çatı": [
        "Ettirgen Çatı", "Edilgen Çatı", "Dönüşlü Çatı", "İşteş Çatı"
    ],
    "Cümle Türleri": [
        "Yapısına Göre Cümle", "Anlamına Göre Cümle", "Yüklemine Göre Cümle"
    ]
}

# Zorluk seviyeleri
ZORLUK_SEVIYELERI = ["Kolay", "Orta", "Zor"]

# ==================== LLM PROMPT ŞABLONLARI ====================
SYSTEM_PROMPT = """Sen bir LGS (Liselere Geçiş Sınavı) Türkçe dersi uzmanısın.
Geçmiş yılların LGS Türkçe sorularını analiz ederek yeni sorular üretiyorsun.

ÖNEMLİ KURALLAR:
1. SADECE Türkçe dersiyle ilgili sorular üret
2. Sorular LGS formatında olmalı (4 seçenekli: A, B, C, D)
3. Her sorunun bir doğru cevabı olmalı
4. Cevap açıklaması detaylı ve öğretici olmalı
5. Türkçe dil bilgisi kurallarına uygun sorular üret
6. Matematik, Fen, Sosyal gibi diğer derslerle ilgili soru ÜRETME
"""

QUESTION_GENERATION_PROMPT = """
Aşağıdaki örnek sorulara benzer, {konu} konusunda {zorluk} zorluk seviyesinde {adet} yeni LGS Türkçe sorusu üret.

ÖRNEK SORULAR:
{ornekler}

ÜRETİLECEK SORU FORMATI:
Her soru için:
1. Soru metni (4 seçenekli: A, B, C, D)
2. Doğru Cevap: (A/B/C/D)
3. Açıklama: (Neden bu cevabın doğru olduğunu açıkla)

Lütfen {adet} adet özgün soru üret.
"""

TOPIC_DETECTION_PROMPT = """
Aşağıdaki Türkçe sorusunun hangi konuya ait olduğunu belirle.

SORU:
{soru}

KONULAR:
{konular}

Sadece konu adını yaz, başka bir şey yazma.
"""

# ==================== KONU DIŞI UYARI ====================
KONU_DISI_UYARI = """
⚠️ Bu sistem sadece LGS Türkçe dersi soruları için tasarlanmıştır.

Matematik, Fen Bilimleri, Sosyal Bilgiler, Din Kültürü, İngilizce gibi 
diğer derslerle ilgili sorulara yanıt veremiyorum.

Lütfen Türkçe dersiyle ilgili bir soru sorun veya soru üretmemi isteyin.
"""

# ==================== UYGULAMA MESAJLARI ====================
KARSILAMA_MESAJI = """
🎓 **LGS Türkçe Soru Tahminleme Modeli**'ne Hoş Geldiniz!

Bu sistem, geçmiş yılların LGS Türkçe sorularından öğrenerek 
yeni ve özgün sorular üretir.

📚 **Yapabileceklerim:**
• Belirli bir konuda yeni soru üretmek
• Farklı zorluk seviyelerinde sorular hazırlamak
• Soruların konu analizini yapmak
• Türkçe konularında açıklama yapmak

🔍 **Örnek Kullanım:**
- "Sözcükte anlam konusunda 3 soru üret"
- "Zor seviyede fiilde çatı sorusu hazırla"
- "Paragraf sorusu oluştur"
"""
