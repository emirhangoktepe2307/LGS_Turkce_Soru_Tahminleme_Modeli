"""
LGS Türkçe Soru Tahminleme Modeli - Yapılandırma Dosyası
Hibrit Model: Veri Analizi + Gemini API Entegrasyonu
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# ==================== TEMEL AYARLAR ====================
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
MODEL_DIR = BASE_DIR / "models"

# .env dosyasını yükle
ENV_FILE = BASE_DIR / ".env"
if ENV_FILE.exists():
    load_dotenv(ENV_FILE)
else:
    # Üst dizindeki .env dosyasını da kontrol et
    PARENT_ENV = BASE_DIR.parent / ".env"
    if PARENT_ENV.exists():
        load_dotenv(PARENT_ENV)

# Dizinleri oluştur
DATA_DIR.mkdir(exist_ok=True)
MODEL_DIR.mkdir(exist_ok=True)

# ==================== API AYARLARI ====================
# Gemini API anahtarı (.env dosyasından okunur)
# .env dosyasında: Gemini_API_Key=your_api_key
# API anahtarı almak için: https://makersuite.google.com/app/apikey
GEMINI_API_KEY = os.getenv("Gemini_API_Key", "BURAYA_API_ANAHTARINIZI_GIRIN")

# ==================== MODEL AYARLARI ====================
# Gemini model seçimi
GEMINI_MODEL = "gemini-2.0-flash"  # veya "gemini-1.5-pro", "gemini-pro"

# ==================== VERİ DOSYALARI ====================
# Ana eğitim verisi
TRAINING_DATA_FILE = str(BASE_DIR / "data.json")
# Üretilen sorular
GENERATED_QUESTIONS_FILE = str(DATA_DIR / "uretilen_sorular.json")

# ==================== API SUNUCU AYARLARI ====================
API_HOST = "0.0.0.0"
API_PORT = 8000

# ==================== TÜRKÇE DERSİ KATEGORİLERİ ====================
# Veri setindeki ana kategoriler
TURKCE_KATEGORILERI = [
    "Paragrafta Anlam",
    "Cümlede Anlam",
    "Sözcükte Anlam",
    "Söz Öbeğinde Anlam",
    "Paragrafta Yapı",
    "Şiirde Anlam"
]

# Zorluk seviyeleri
ZORLUK_SEVIYELERI = ["kolay", "orta", "zor"]

# ==================== LLM PROMPT ŞABLONLARI ====================
SYSTEM_PROMPT = """Sen bir LGS (Liselere Geçiş Sınavı) Türkçe dersi uzmanısın.
Geçmiş yılların LGS Türkçe sorularını analiz ederek 2026 sınavı için yeni sorular tahminliyorsun.

ÖNEMLİ KURALLAR:
1. SADECE Türkçe dersiyle ilgili sorular üret
2. Sorular LGS formatında olmalı (4 seçenekli: A, B, C, D)
3. Her sorunun bir doğru cevabı olmalı
4. Cevap açıklaması detaylı ve öğretici olmalı
5. Matematik, Fen, Sosyal gibi diğer derslerle ilgili soru ÜRETME
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
2026 sınavı için yeni soru tahminleri üretir.

📚 **Yapabileceklerim:**
• 2026 LGS için soru tahminlemesi yapmak
• Kategori bazlı yeni sorular üretmek
• Trend analizleri sunmak
• Soruları analiz etmek

🔍 **API Endpoints:**
- POST /api/v1/generate - Yeni soru üret
- GET /api/v1/predict/trends - 2026 tahminleri
- POST /api/v1/analyze - Soru analizi
- GET /api/v1/statistics - İstatistikler
"""
