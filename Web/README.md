# LGS Analiz ve Tahmin Asistanı - Web Uygulaması

Bu klasör, LGS Türkçe soru analizi ve tahmin sistemi için geliştirilmiş modern web uygulamasını içerir.

## 🚀 Teknolojiler

- **Next.js 14** (App Router)
- **TypeScript**
- **Tailwind CSS**
- **Lucide React** (İkonlar)
- **Recharts** (Grafikler)

## 📁 Proje Yapısı

```
Web/
├── app/                    # Next.js App Router sayfaları
│   ├── dashboard/         # Dashboard sayfaları
│   ├── layout.tsx         # Ana layout
│   ├── page.tsx           # Ana sayfa (Landing Page)
│   └── globals.css        # Global stiller
├── components/            # React bileşenleri
│   ├── dashboard/         # Dashboard bileşenleri
│   └── ui/                # UI bileşenleri (Button, Card, Input)
├── lib/                   # Yardımcı fonksiyonlar
│   └── utils.ts
├── package.json           # Bağımlılıklar
├── tsconfig.json          # TypeScript yapılandırması
├── tailwind.config.ts     # Tailwind CSS yapılandırması
└── next.config.js         # Next.js yapılandırması
```

## 🛠️ Kurulum

```bash
cd Web
npm install
npm run dev
```

Uygulama [http://localhost:3000](http://localhost:3000) adresinde çalışacaktır.

## 📄 Sayfalar

- **Ana Sayfa (`/`)**: Landing page - Proje tanıtımı ve özellikler
- **Dashboard (`/dashboard`)**: Kullanıcı paneli
  - Tahminler
  - Soru Çöz
  - İstatistiklerim
  - Hata Analizi

## 🎨 Özellikler

- ✅ Modern ve responsive tasarım
- ✅ Mavi-beyaz renk teması
- ✅ Sidebar navigasyon
- ✅ Grafik gösterimi (Recharts)
- ✅ Mock veriler ile çalışan arayüz

## 📝 Notlar

- Şu anda tüm veriler mock (sahte) verilerdir
- Backend API entegrasyonu henüz yapılmamıştır
- ML modeli entegrasyonu planlanmaktadır

## 🔗 İlgili Projeler

Bu web uygulaması, [LGS Türkçe Soru Tahminleme Modeli](https://github.com/emirhangoktepe2307/LGS_Turkce_Soru_Tahminleme_Modeli) projesinin frontend kısmıdır.

