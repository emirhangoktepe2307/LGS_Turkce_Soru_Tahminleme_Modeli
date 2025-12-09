# 📚 LGS Türkçe Soru Tahminleme Modeli

**LLM (Large Language Model) Tabanlı Yapay Zeka Soru Üretim ve Tahminleme Sistemi**

## 🎯 Proje Hakkında

Bu proje, LGS (Liselere Geçiş Sınavı) Türkçe dersi için LLM tabanlı soru tahminleme ve üretim sistemidir. Google Gemini API kullanarak geçmiş yılların sorularından öğrenir ve yeni, özgün sorular üretir.

### 🏗️ Mimari

```
┌─────────────────────────────────────────────────────┐
│                    Kullanıcı Arayüzü                │
│                  (Streamlit Web App)                 │
└─────────────────────┬───────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────┐
│                   LLM Model                         │
│              (Google Gemini API)                    │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │
│  │Soru Üretimi │  │Konu Tahmini │  │   Analiz    │ │
│  └─────────────┘  └─────────────┘  └─────────────┘ │
└─────────────────────┬───────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────┐
│                  Veri İşleme                        │
│              (Data Processor)                       │
│  ┌─────────────────────────────────────────────┐   │
│  │         LGS Türkçe Soru Veritabanı          │   │
│  │           (JSON - Eğitim Verisi)            │   │
│  └─────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

### Özellikler

- 🤖 **LLM Tabanlı Soru Üretimi**: Gemini API ile akıllı soru üretimi
- 🎯 **Konu Tahmini**: Soruların hangi konuya ait olduğunu tahmin eder
- 📊 **Soru Analizi**: Detaylı soru analizi ve çözüm stratejileri
- 💬 **Sohbet Botu**: Türkçe konularında yardımcı asistan
- 📖 **Konu Anlatımı**: Detaylı konu açıklamaları
- 🎓 **Sadece Türkçe**: Diğer derslere cevap vermez

## 🛠️ Kurulum

### Gereksinimler

- Python 3.9 veya üstü
- Google Gemini API anahtarı

### Adım Adım Kurulum

1. **Gerekli kütüphaneleri yükleyin:**

```bash
pip install -r requirements.txt
```

2. **Gemini API Anahtarını Ayarlayın:**

`config.py` dosyasını açın ve API anahtarınızı girin:

```python
GEMINI_API_KEY = "sizin_api_anahtariniz"
```

API anahtarı almak için: https://makersuite.google.com/app/apikey

3. **Uygulamayı Çalıştırın:**

```bash
streamlit run app.py
```

## 📁 Dosya Yapısı

```
Model_Mimarisi/
├── app.py                    # Streamlit web arayüzü
├── config.py                 # Yapılandırma ve prompt şablonları
├── llm_model.py             # LLM model sınıfı (Gemini API)
├── data_processor.py        # Veri işleme modülü
├── lgs_turkce_sorulari.json # Eğitim verisi (örnek sorular)
├── requirements.txt         # Python bağımlılıkları
├── Dockerfile               # Docker yapılandırması
├── docker-compose.yml       # Docker Compose
├── run.bat                  # Windows başlatma scripti
├── run.ps1                  # PowerShell başlatma scripti
└── README.md                # Bu dosya
```

## 🚀 Kullanım

### Web Arayüzü

```bash
streamlit run app.py
```

Tarayıcınızda `http://localhost:8501` adresine gidin.

### Python API

```python
from llm_model import LGSTurkceModel

# Modeli başlat
model = LGSTurkceModel()

# Soru üret
sorular = model.generate_questions(
    konu="Sözcükte Anlam",
    zorluk="Orta",
    adet=3
)
print(sorular)

# Konu tahmini yap
konu = model.predict_topic("Aşağıdaki cümlelerin hangisinde zıt anlamlı sözcükler kullanılmıştır?")
print(f"Tahmin: {konu}")

# Soru analizi
analiz = model.analyze_question("...")
print(analiz)
```

## 📚 Desteklenen Konular

| Ana Konu | Alt Konular |
|----------|-------------|
| Sözcükte Anlam | Eş Anlam, Zıt Anlam, Mecaz Anlam, Sesteş, Deyimler |
| Cümlede Anlam | Öznel/Nesnel Yargı, Neden-Sonuç, Koşul-Sonuç |
| Paragrafta Anlam | Ana Düşünce, Yardımcı Düşünce, Başlık |
| Dil Bilgisi | Fiil Kipleri, İsim Tamlaması, Sıfatlar, Zarflar |
| Yazım Kuralları | Büyük Harf, Ki/De Yazımı |
| Noktalama İşaretleri | Virgül, İki Nokta, Noktalı Virgül |
| Söz Sanatları | Benzetme, Kişileştirme, Abartma |
| Anlatım Bozuklukları | Gereksiz Sözcük, Özne-Yüklem Uyumu |
| Fiilde Çatı | Ettirgen, Edilgen, Dönüşlü, İşteş |
| Cümle Türleri | Basit, Birleşik, Sıralı |

## ⚙️ Yapılandırma

`config.py` dosyasından ayarları özelleştirebilirsiniz:

```python
# API Ayarları
GEMINI_API_KEY = "your-api-key"
GEMINI_MODEL = "gemini-1.5-flash"  # veya "gemini-1.5-pro"

# Eğitim Ayarları
TRAINING_CONFIG = {
    "epochs": 3,
    "batch_size": 8,
    "learning_rate": 2e-5,
    "max_length": 512
}
```

## 🐳 Docker ile Çalıştırma

```bash
docker-compose up --build
```

## 🔒 Güvenlik

- API anahtarınızı asla paylaşmayın
- Üretim ortamında çevre değişkenleri kullanın:

```bash
export GEMINI_API_KEY="your-api-key"
```

## 📄 Lisans

MIT License

---

**⚠️ Not:** Bu sistem sadece LGS Türkçe dersi için tasarlanmıştır. 
Matematik, Fen Bilimleri, Sosyal Bilgiler gibi diğer dersler için soru üretmez.
