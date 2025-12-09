# 📚 LGS Türkçe Soru Üretici

**RAG (Retrieval-Augmented Generation) Mimarisi ile Yapay Zeka Destekli Soru Üretim Sistemi**

## 🎯 Proje Hakkında

Bu proje, LGS (Liselere Geçiş Sınavı) Türkçe dersi için yapay zeka destekli soru üretim sistemidir. Google Gemini API kullanarak geçmiş yılların sorularını analiz eder ve yeni, özgün sorular üretir.

### Özellikler

- 🤖 **AI Tabanlı Soru Üretimi**: Gemini API ile akıllı soru üretimi
- 📊 **Vektör Veritabanı**: ChromaDB ile semantik soru araması
- 🎓 **Konu Odaklı**: Sadece Türkçe dersine özel, diğer derslere cevap vermez
- 📝 **Quiz Modu**: İnteraktif sınav simülasyonu
- 💬 **Sohbet Botu**: Türkçe konularında yardımcı asistan
- 📖 **Konu Anlatımı**: Detaylı konu açıklamaları

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

3. **Veritabanını Başlatın:**

```bash
python turkce_chroma_setup.py
```

4. **Uygulamayı Çalıştırın:**

```bash
streamlit run app.py
```

## 📁 Dosya Yapısı

```
Hafta-1/
├── app.py                    # Streamlit web arayüzü
├── config.py                 # Yapılandırma ayarları
├── gemini_rag.py            # RAG sistemi ve Gemini entegrasyonu
├── turkce_chroma_setup.py   # ChromaDB veritabanı kurulumu
├── soru_uretici.py          # Soru yönetim modülü
├── lgs_turkce_sorulari.json # Örnek soru veritabanı
├── requirements.txt         # Python bağımlılıkları
├── Dockerfile               # Docker yapılandırması
├── docker-compose.yml       # Docker Compose
└── README.md                # Bu dosya
```

## 🚀 Kullanım

### Web Arayüzü

```bash
streamlit run app.py
```

Tarayıcınızda `http://localhost:8501` adresine gidin.

### Komut Satırı

```python
from gemini_rag import TurkceRAG
from turkce_chroma_setup import initialize_database

# Veritabanını başlat
client, collection = initialize_database()

# RAG sistemini oluştur
rag = TurkceRAG(collection=collection)

# Soru üret
sorular = rag.generate_questions(
    konu="Sözcükte Anlam",
    alt_konu="Eş Anlamlı Sözcükler",
    zorluk="Orta",
    adet=3
)
print(sorular)
```

## 📚 Desteklenen Konular

| Ana Konu | Alt Konular |
|----------|-------------|
| Sözcükte Anlam | Eş Anlam, Zıt Anlam, Mecaz Anlam, Sesteş Sözcükler |
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

# Veritabanı Ayarları
CHROMA_PERSIST_DIR = "./chroma_db"
COLLECTION_NAME = "lgs_turkce_sorulari"

# Embedding Model
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
```

## 🐳 Docker ile Çalıştırma

```bash
docker-compose up --build
```

## 🔒 Güvenlik Notu

- API anahtarınızı asla paylaşmayın
- Üretim ortamında çevre değişkenleri kullanın:

```bash
export GEMINI_API_KEY="your-api-key"
```

## 🐛 Sorun Giderme

### "API anahtarı geçersiz" hatası
- API anahtarınızın doğru olduğundan emin olun
- https://makersuite.google.com/app/apikey adresinden yeni anahtar alın

### "ChromaDB bağlantı hatası"
- `chroma_db` klasörünü silip tekrar başlatın
- Python sürümünüzün 3.9+ olduğundan emin olun

### "Module not found" hatası
```bash
pip install -r requirements.txt --upgrade
```

## 📄 Lisans

Bu proje eğitim amaçlı geliştirilmiştir.

---

**Not:** Bu sistem sadece LGS Türkçe dersi için tasarlanmıştır. Matematik, Fen Bilimleri, Sosyal Bilgiler gibi diğer dersler için soru üretmez.

