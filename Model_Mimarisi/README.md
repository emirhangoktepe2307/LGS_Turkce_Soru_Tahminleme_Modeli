# 🎓 LGS Türkçe Soru Tahminleme Modeli

**Hibrit AI Model**: Veri Analizi + Google Gemini API

Bu proje, geçmiş yılların LGS Türkçe sorularını analiz ederek 2026 sınavı için yeni soru tahminleri üretir.

## 📁 Proje Yapısı

```
Model_Mimarisi/
├── model/                      # AI Model Modülleri
│   ├── __init__.py
│   ├── data_analyzer.py       # Veri analizi ve pattern çıkarma
│   ├── gemini_client.py       # Gemini API entegrasyonu
│   └── question_predictor.py  # Hibrit tahminleme sistemi
├── api/                        # REST API
│   ├── __init__.py
│   └── endpoints.py           # FastAPI endpoints
├── data.json                   # Eğitim verisi (185+ LGS sorusu)
├── main.py                     # Ana uygulama
├── config.py                   # Yapılandırma
├── requirements.txt            # Bağımlılıklar
└── .env                        # API anahtarları (oluşturulmalı)
```

## 🚀 Kurulum

### 1. Bağımlılıkları Yükleyin

```bash
cd Model_Mimarisi
pip install -r requirements.txt
```

### 2. API Anahtarını Ayarlayın

`.env` dosyası oluşturun:

```env
Gemini_API_Key=your_gemini_api_key_here
```

> API anahtarı almak için: https://makersuite.google.com/app/apikey

## 🖥️ Kullanım

### REST API Sunucusu (Web Entegrasyonu İçin)

```bash
python main.py --api
```

Sunucu başladığında:
- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **API Base**: http://localhost:8000/api/v1

### CLI Modu (Test için)

```bash
python main.py --cli
```

## 📡 REST API Endpoints

### Temel Endpoints

| Endpoint | Method | Açıklama |
|----------|--------|----------|
| `/api/v1/status` | GET | Model durumu |
| `/api/v1/categories` | GET | Desteklenen kategoriler |
| `/api/v1/statistics` | GET | Veri istatistikleri |

### Soru Üretimi

| Endpoint | Method | Açıklama |
|----------|--------|----------|
| `/api/v1/generate` | POST | Yeni soru üret |
| `/api/v1/predict/trends` | GET | 2026 trend tahminleri |
| `/api/v1/analyze` | POST | Soru analizi |
| `/api/v1/sample/{category}` | GET | Örnek sorular |

### Örnek İstekler

#### Soru Üretme

```bash
curl -X POST "http://localhost:8000/api/v1/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "category": "Paragrafta Anlam",
    "count": 5,
    "difficulty": "orta"
  }'
```

#### 2026 Trend Tahminleri

```bash
curl "http://localhost:8000/api/v1/predict/trends"
```

#### Soru Analizi

```bash
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "question_text": "Aşağıdaki cümlelerin hangisinde neden-sonuç ilişkisi vardır?"
  }'
```

## 📊 Veri Seti

`data.json` dosyası şunları içerir:
- **185+ LGS sorusu** (2018-2021 yılları)
- **MEB örnek soruları**
- **6 ana kategori**: Paragrafta Anlam, Cümlede Anlam, Sözcükte Anlam, Söz Öbeğinde Anlam, Paragrafta Yapı, Şiirde Anlam

### Veri Yapısı

```json
{
  "Ticket_ID": ["LGS-2018-C-001", ...],
  "Kategori": ["Söz Öbeğinde Anlam", ...],
  "Alt Başlık": ["Sözcük Grubu Yorumlama", ...],
  "Metinler": ["Metin içeriği...", ...],
  "Soru Kökleri": ["Soru metni...", ...],
  "Cevaplar": ["Doğru cevap ve açıklama...", ...],
  "Keywords": [["anahtar", "kelimeler"], ...]
}
```

## 🔄 Hibrit Model Çalışma Prensibi

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   data.json     │────▶│  DataAnalyzer   │────▶│ Pattern & Stats │
│  (LGS Soruları) │     │ (Veri Analizi)  │     │   Extraction    │
└─────────────────┘     └─────────────────┘     └────────┬────────┘
                                                         │
                                                         ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Yeni Sorular   │◀────│  GeminiClient   │◀────│ Context + Few   │
│   (Tahminler)   │     │ (Soru Üretimi)  │     │  Shot Examples  │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

1. **Veri Analizi**: Geçmiş LGS soruları analiz edilir
2. **Pattern Çıkarma**: Soru kalıpları ve trendler belirlenir
3. **Context Oluşturma**: Gemini için zengin bağlam hazırlanır
4. **Soru Üretimi**: Gemini API ile özgün sorular üretilir

## 🌐 Web Entegrasyonu

Web sitesinde API'yi şu şekilde kullanabilirsiniz:

```javascript
// Soru üret
async function generateQuestions() {
  const response = await fetch('http://localhost:8000/api/v1/generate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      category: 'Paragrafta Anlam',
      count: 5,
      difficulty: 'orta'
    })
  });
  const data = await response.json();
  return data.data.generated_questions;
}

// Trend tahminleri al
async function getTrends() {
  const response = await fetch('http://localhost:8000/api/v1/predict/trends');
  const data = await response.json();
  return data.data.trend_predictions;
}
```

## 📝 Notlar

- Model sadece **Türkçe dersi** soruları üretir
- Diğer derslerle ilgili istekler reddedilir
- Her istekte 1-10 arası soru üretilebilir
- Zorluk seviyeleri: `kolay`, `orta`, `zor`

## 📄 Lisans

Bu proje eğitim amaçlıdır.
