# LGS Soru Tahmin Backend API

Python FastAPI kullanılarak geliştirilmiş backend API iskeleti.

## Özellikler

- ✅ Soru oluşturma endpoint'leri
- ✅ Profil istatistikleri
- ✅ Grafik verileri (haftalık, doğru cevaplar)
- ✅ Son çözülen sorular listesi
- ✅ CORS desteği
- ✅ Pydantic modelleri ile veri doğrulama
- ✅ Mock data ile test edilebilir yapı

## Kurulum

1. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

2. API'yi çalıştırın:
```bash
python main.py
```

veya

```bash
uvicorn main:app --reload
```

API `http://localhost:8000` adresinde çalışacaktır.

## API Dokümantasyonu

API çalıştıktan sonra şu adreslerden dokümantasyona erişebilirsiniz:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Endpoint'ler

### Konular
- `GET /api/konular/{soru_tipi}` - Soru tipine göre konuları döner

### Soru Oluşturma
- `POST /api/sorular/olustur` - Seçilen konu ve yıla göre soru oluşturur

### Profil
- `GET /api/profil/istatistikler` - Kullanıcı profil istatistikleri
- `GET /api/profil/grafik/haftalik` - Haftalık soru çözüm grafiği
- `GET /api/profil/grafik/dogru-cevaplar` - Doğru cevaplar grafiği
- `GET /api/profil/son-cozulen-sorular` - Son çözülen sorular listesi

### Health Check
- `GET /` - API root
- `GET /health` - Health check

## Notlar

- Şu anda tüm veriler mock (sahte) veridir
- Veritabanı bağlantısı henüz yapılmamıştır
- Frontend ile bağlantı için CORS ayarları yapılmıştır

