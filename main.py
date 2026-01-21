"""
LGS Soru Tahmin Backend API
FastAPI ile geliştirilmiş backend iskeleti
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import List
from datetime import datetime, timedelta
import random
import os

from models import (
    SoruOlusturRequest,
    SoruResponse,
    ProfilIstatistikResponse,
    GrafikVeriResponse,
    SonCozulenSoruResponse,
    KonularResponse,
    KullaniciBilgiResponse,
    SoruTipi
)

import google.generativeai as genai
from dotenv import load_dotenv
import json
from pymongo import MongoClient
from passlib.context import CryptContext
from pydantic import BaseModel

# .env dosyasını yükle (API anahtarı için)
load_dotenv()

GEMINI_API_KEY = os.getenv("Gemini_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

MONGODB_URI = os.getenv("MONGODB_URI")

# MongoDB Setup
try:
    if MONGODB_URI:
        client = MongoClient(MONGODB_URI)
        db = client["lgs_soru_tahmin"]
        users_collection = db["users"]
        print("MongoDB Bağlantısı Başarılı")
    else:
        print("UYARI: MONGODB_URI bulunamadı!. Veritabanı işlemleri çalışmayabilir.")
        db = None
        users_collection = None
except Exception as e:
    print(f"MongoDB Bağlantı Hatası: {e}")
    db = None
    users_collection = None

# Password Hashing
# bcrypt bazen Windows'ta sorun çıkarabiliyor, pbkdf2_sha256 daha güvenli bir alternatif olabilir bu ortamda.
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

class RegisterRequest(BaseModel):
    email: str
    username: str
    password: str

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    # Model yapılandırması
    model = genai.GenerativeModel('gemini-flash-latest')
else:
    print("UYARI: Gemini_API_KEY bulunamadı! Mock veri kullanılacak.")
    model = None

# FastAPI uygulaması oluştur
app = FastAPI(
    title="LGS Soru Tahmin API",
    description="LGS Türkçe soru oluşturma ve profil yönetimi API'si",
    version="1.0.0"
)

# Statik dosyaları sunmak için yapılandırma
# 'static' klasörünün varlığını kontrol et, yoksa oluştur (güvenlik için)
if not os.path.exists("static"):
    os.makedirs("static")


# CORS ayarları - Frontend ile haberleşme için
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production'da spesifik domain'ler belirtilmeli
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock veri - Konular
CUMLEDE_KONULAR = [
    "Anlam İlişkileri",
    "Neden - Sonuç",
    "Amaç - Sonuç",
    "Karşılaştırma",
    "Koşul - Sonuç",
    "Örtülü Anlam",
    "Düşünceyi Geliştirme Yolları",
    "Tanım",
    "Örneklendirme",
    "Açıklama",
    "Tanık Gösterme",
    "Sayısal Veri Kullanma"
]

PARAGRAF_KONULAR = [
    "Ana Düşünce",
    "Yardımcı Düşünce",
    "Paragrafta Akışı Bozan Cümle",
    "Boşluk Doldurma",
    "Anlatım Bozukluğu",
    "Paragrafta Yapı",
    "Paragraf Tamamlama",
    "Bakış Açısı"
]

# Mock veri - Soru örnekleri (Liste formatında)
MOCK_SORULAR = {
    "cumlede": {
        "Anlam İlişkileri": [
            {
                "soru_metni": "Aşağıdaki cümlelerin hangisinde 'sebep-sonuç' ilişkisi vardır?",
                "secenekler": ["A) Seni görmek için ta İstanbul'dan geldim.", "B) Yağmur yağınca maç iptal edildi.", "C) Düzenli çalışırsan kazanırsın.", "D) Bu kitap, diğerinden daha sürükleyici."],
                "dogru_cevap": "B) Yağmur yağınca maç iptal edildi."
            },
            {
                "soru_metni": "Hangi cümlede 'amaç-sonuç' anlamı ağır basmaktadır?",
                "secenekler": ["A) Yolu bulabilmek için haritaya baktı.", "B) Kar yağarsa okullar tatil olur.", "C) Çok yediği için midesi ağrıdı.", "D) Gözleri deniz mavisiydi."],
                "dogru_cevap": "A) Yolu bulabilmek için haritaya baktı."
            },
            {
                "soru_metni": "'Sınavı kazanmak ______ kursa gidiyor.' cümlesinde boşluğa ne gelirse amaç-sonuç ilişkisi oluşur?",
                "secenekler": ["A) sebebiyle", "B) olduğundan", "C) üzere", "D) şayet"],
                "dogru_cevap": "C) üzere"
            }
        ],
        "Neden - Sonuç": [
            {
                "soru_metni": "Aşağıdakilerden hangisi neden-sonuç cümlesidir?",
                "secenekler": ["A) Ekmek almak üzere fırına gitti.", "B) Kar yağdığı için okullar tatil oldu.", "C) Konuşmak üzere kürsüye çıktı.", "D) Kilo vermek için diyet yapıyor."],
                "dogru_cevap": "B) Kar yağdığı için okullar tatil oldu."
            },
            {
                "soru_metni": "Hangisinde bir eylemin gerçekleşmesi bir nedene bağlanmıştır?",
                "secenekler": ["A) Erken kalkarsan yetişirsin.", "B) Seni sevdiğimden katlanıyorum bunlara.", "C) Bildiğim kadarıyla o gelmeyecek.", "D) Kitap okumak ufku açar."],
                "dogru_cevap": "B) Seni sevdiğimden katlanıyorum bunlara."
            },
            {
                "soru_metni": "'Geç kaldığı için derse giremedi.' cümlesindeki anlam ilişkisi aşağıdakilerden hangisidir?",
                "secenekler": ["A) Amaç-Sonuç", "B) Koşul-Sonuç", "C) Neden-Sonuç", "D) Karşılaştırma"],
                "dogru_cevap": "C) Neden-Sonuç"
            }
        ],
        "Amaç - Sonuç": [
            {
                "soru_metni": "Aşağıdaki cümlelerin hangisinde amaç-sonuç ilişkisi vardır?",
                "secenekler": ["A) Yağmur yağdığı için ıslandık.", "B) Seni görmek üzere buraya geldim.", "C) Çok çalışırsan başarırsın.", "D) Evden çıkınca kapıyı kilitledi."],
                "dogru_cevap": "B) Seni görmek üzere buraya geldim."
            },
            {
                "soru_metni": "Hangisi bir amaç bildirmektedir?",
                "secenekler": ["A) Kilo vermek için spor yapıyor.", "B) Uykusuzluktan gözleri kızarmıştı.", "C) Zil çalınca herkes dışarı çıktı.", "D) Hava soğuk olursa montunu giy."],
                "dogru_cevap": "A) Kilo vermek için spor yapıyor."
            },
            {
                "soru_metni": "'Borçlarını ödemek ______ evini sattı.' cümlesinde boşluğa hangisi gelirse amaç anlamı taşır?",
                "secenekler": ["A) dolayı", "B) olduğundan", "C) maksadıyla", "D) yüzünden"],
                "dogru_cevap": "C) maksadıyla"
            }
        ],
        "Koşul - Sonuç": [
            {
                "soru_metni": "Hangi cümlede eylemin gerçekleşmesi bir şarta bağlıdır?",
                "secenekler": ["A) Ödevini yaparsan dışarı çıkabilirsin.", "B) Dün akşam sinemaya gittik.", "C) Kitap okumayı çok severim.", "D) Okula gitmek için erken kalktı."],
                "dogru_cevap": "A) Ödevini yaparsan dışarı çıkabilirsin."
            },
             {
                "soru_metni": "'İstediklerini alırım ______ kardeşinle iyi geçineceksin.' cümlesinde boşluğa ne gelmelidir?",
                "secenekler": ["A) ama", "B) fakat", "C) yeter ki", "D) çünkü"],
                "dogru_cevap": "C) yeter ki"
            },
            {
                "soru_metni": "Aşağıdakilerden hangisi koşul-sonuç cümlesidir?",
                "secenekler": ["A) Düzenli çalışmak başarı getirir.", "B) Erken gelirsen görüşürüz.", "C) Seni gördüğüme sevindim.", "D) Hava kararınca sokak lambaları yandı."],
                "dogru_cevap": "B) Erken gelirsen görüşürüz."
            }
        ]
    },
    "paragrafta": {
        "Ana Düşünce": [
             {
                "soru_metni": "Bir paragrafın yazılma amacı ve okuyucuya verilmek istenen temel mesaj aşağıdakilerden hangisidir?",
                "secenekler": ["A) Yardımcı Düşünce", "B) Konu", "C) Ana Düşünce", "D) Başlık"],
                "dogru_cevap": "C) Ana Düşünce"
            },
            {
                "soru_metni": "Yazarın asıl vurgulamak istediği, okuyucunun 'Burada anlatılan nedir?' sorusuna değil, 'Burada verilmek istenen mesaj nedir?' sorusuna verdiği cevap hangisidir?",
                "secenekler": ["A) Ana Düşünce", "B) Konu", "C) Anahtar Kelime", "D) Giriş Cümlesi"],
                "dogru_cevap": "A) Ana Düşünce"
            },
            {
                "soru_metni": "Paragrafın en genel yargısı genellikle hangisidir?",
                "secenekler": ["A) Sonuç bölümünde verilen ana düşünce", "B) İlk cümledeki örnek", "C) Ortadaki detaylar", "D) Yazarın biyografisi"],
                "dogru_cevap": "A) Sonuç bölümünde verilen ana düşünce"
            }
        ],
        "Boşluk Doldurma": [
            {
                "soru_metni": "Dil, kültürün taşıyıcısıdır. Bir milletin geçmişi, değerleri ve birikimleri dil ______ nesilden nesile aktarılır.",
                "secenekler": ["A) ile", "B) için", "C) kadar", "D) göre"],
                "dogru_cevap": "A) ile"
            },
            {
                "soru_metni": "Başarı, sadece yetenekle ilgili değildir; ______ çalışma ve azim gerektirir.",
                "secenekler": ["A) fakat", "B) veya", "C) aynı zamanda", "D) lakin"],
                "dogru_cevap": "C) aynı zamanda"
            },
            {
                "soru_metni": "Kitaplar, bize hiç gitmediğimiz yerleri gezdirir, tanımadığımız insanlarla tanıştırır. ______, kitap okumak ufkumuzu genişletir.",
                "secenekler": ["A) Kısacası", "B) Oysa", "C) Çünkü", "D) Fakat"],
                "dogru_cevap": "A) Kısacası"
            }
        ],
        "Yardımcı Düşünce": [
             {
                "soru_metni": "Bu paragraftan çıkarılabilecek yardımcı düşüncelerden biri aşağıdakilerden hangisidir?",
                "secenekler": ["A) Ana fikirle çelişir.", "B) Ana fikri destekler.", "C) Konudan bağımsızdır.", "D) En kapsamlı yargıdır."],
                "dogru_cevap": "B) Ana fikri destekler."
            },
            {
                "soru_metni": "Paragrafta değinilmeyen düşünce hangisidir sorusu neyi bulmaya yöneliktir?",
                "secenekler": ["A) Ana Düşünce", "B) Yardımcı Düşünce", "C) Başlık", "D) Konu"],
                "dogru_cevap": "B) Yardımcı Düşünce"
            },
             {
                "soru_metni": "Aşağıdakilerden hangisi bir paragrafın yardımcı düşüncesi olamaz?",
                "secenekler": ["A) Yazarın savunduğu tezi destekleyen örnek", "B) Konunun farklı bir yönü", "C) Ana düşüncenin ta kendisi", "D) İleri sürülen kanıtlar"],
                "dogru_cevap": "C) Ana düşüncenin ta kendisi"
            }
        ]
    }
}

# Mock MEB Çıkmış Sorular (Benzeri)
MEB_QUESTIONS_MOCK = {
    "paragrafta": [
        {
            "soru_metni": "(2020 LGS Benzeri) Bu metnin ana düşüncesi aşağıdakilerden hangisidir?",
            "secenekler": ["A) Kitap okumak ufku açar.", "B) Sanat toplum içindir.", "C) Başarı çalışmaktan geçer.", "D) Dostluk fedakarlık ister."],
            "dogru_cevap": "A) Kitap okumak ufku açar."
        },
        {
            "soru_metni": "(2021 MEB Örnek) Numaralanmış cümlelerin hangisinde neden-sonuç ilişkisi vardır?",
            "secenekler": ["A) I", "B) II", "C) III", "D) IV"],
            "dogru_cevap": "B) II"
        },
        {
            "soru_metni": "(2019 LGS Benzeri) Paragrafta altı çizili sözle anlatılmak istenen nedir?",
            "secenekler": ["A) Özgün olmak", "B) Akıcı olmak", "C) Tutarlı olmak", "D) Yalın olmak"],
            "dogru_cevap": "A) Özgün olmak"
        }
    ],
    "cumlede": [
        {
            "soru_metni": "(2022 LGS Benzeri) Aşağıdaki cümlelerin hangisinde 'karşılaştırma' yapılmıştır?",
            "secenekler": ["A) Bu kitap diğerinden daha sürükleyici.", "B) Yarın sinemaya gideceğiz.", "C) Sabah erkenden uyandım.", "D) Ödevlerimi bitirdim."],
            "dogru_cevap": "A) Bu kitap diğerinden daha sürükleyici."
        },
        {
            "soru_metni": "(2020 MEB Örnek) Hangi cümlede 'amaç-sonuç' ilişkisi vardır?",
            "secenekler": ["A) Seni görmek için geldim.", "B) Yağmur yağdığı için ıslandım.", "C) Çok çalıştığım için yoruldum.", "D) Geç kaldığım için özür dilerim."],
            "dogru_cevap": "A) Seni görmek için geldim."
        },
         {
            "soru_metni": "(2018 LGS Benzeri) Bu cümleden kesin olarak çıkarılabilecek yargı hangisidir?",
            "secenekler": ["A) Yarışmaya sadece 8. sınıflar katıldı.", "B) Yarışma geçen yıl da yapıldı.", "C) Ödül töreni yarın yapılacak.", "D) Okulun en başarılı öğrencisi Ali'dir."],
            "dogru_cevap": "A) Yarışmaya sadece 8. sınıflar katıldı."
        }
    ]
}


# ==================== KONULAR ENDPOINT'LERİ ====================

@app.get("/api/konular/{soru_tipi}", response_model=KonularResponse)
async def konulari_getir(soru_tipi: SoruTipi):
    # ... (Burada değişiklik yok, önceki kod aynen kalıyor)
    if soru_tipi == SoruTipi.CUMLEDE:
        return KonularResponse(konular=CUMLEDE_KONULAR, soru_tipi="cumlede")
    else:
        return KonularResponse(konular=PARAGRAF_KONULAR, soru_tipi="paragrafta")




# ==================== KULLANICI İŞLEMLERİ ====================

@app.post("/api/register")
async def register_user(user: RegisterRequest):
    if users_collection is None:
        raise HTTPException(status_code=503, detail="Veritabanı bağlantısı yok")

    # Check if user exists
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Bu email zaten kayıtlı")
    if users_collection.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Bu kullanıcı adı zaten alınmış")

    # Hash password
    hashed_password = pwd_context.hash(user.password)

    # Create user
    new_user = {
        "email": user.email,
        "username": user.username,
        "password": hashed_password,
        "created_at": datetime.now()
    }
    
    try:
        users_collection.insert_one(new_user)
        return {"message": "Kayıt başarılı"}
    except Exception as e:
        print(f"Kayıt Hatası: {e}")
        raise HTTPException(status_code=500, detail="Kayıt sırasında hata oluştu")

class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/api/login")
async def login_user(user: LoginRequest):
    if users_collection is None:
        raise HTTPException(status_code=503, detail="Veritabanı bağlantısı yok")

    # Find user by username
    db_user = users_collection.find_one({"username": user.username})
    if not db_user:
        raise HTTPException(status_code=400, detail="Kullanıcı adı veya şifre hatalı")

    # Verify password
    if not pwd_context.verify(user.password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Kullanıcı adı veya şifre hatalı")

    return {"message": "Giriş başarılı", "username": db_user["username"]}


# ==================== MEB ÇIKMIŞ SORULAR ENDPOINT'İ ====================


@app.get("/api/meb-questions")
async def get_meb_questions(topic: str):
    """
    Belirtilen konu için MEB çıkmış soru benzerlerini döner.
    Önce Mock veritabanına bakar, yoksa Gemini ile üretmeye çalışır (fallback).
    """
    
    # 1. Konu Listelerinde Arama Yap
    if topic in CUMLEDE_KONULAR:
        return MEB_QUESTIONS_MOCK.get("cumlede", {})
    
    if topic in PARAGRAF_KONULAR:
        return MEB_QUESTIONS_MOCK.get("paragrafta", {})

    # 2. String Eşleşmesi (Fallback)
    normalized_topic = topic.lower()
    
    # "paragraf" kelimesi geçiyorsa paragraf sorularını dön
    if "paragraf" in normalized_topic:
        return MEB_QUESTIONS_MOCK.get("paragrafta", {})
    
    # "cümle" veya "cumle" geçiyorsa
    if "cümle" in normalized_topic or "cumle" in normalized_topic:
         return MEB_QUESTIONS_MOCK.get("cumlede", {})

    # Hiçbir şey bulunamazsa varsayılan olarak paragraf sorularını dön (boş görünmesin) veya boş dön
    return MEB_QUESTIONS_MOCK.get("paragrafta", {})


@app.post("/api/sorular/olustur", response_model=List[SoruResponse])
async def soru_olustur(request: SoruOlusturRequest):
    """
    Seçilen konu ve yıla göre soru oluşturur
    """
    # Konu kontrolü
    if request.soru_tipi == SoruTipi.CUMLEDE:
        if request.konu not in CUMLEDE_KONULAR:
            raise HTTPException(status_code=400, detail="Geçersiz konu seçimi")
    else:
        if request.konu not in PARAGRAF_KONULAR:
            raise HTTPException(status_code=400, detail="Geçersiz konu seçimi")
    
    # Veritabanına Kayıt (Aktivite Logu)
    if users_collection is not None and request.username:
        try:
            db.predictions.insert_one({
                "username": request.username,
                "konu": request.konu,
                "yil": request.yil,
                "soru_tipi": request.soru_tipi.value,
                "tarih": datetime.now()
            })
        except Exception as e:
            print(f"DB Log Hatası: {e}")

    # Soru havuzundan soruları çek
    soru_tipi_str = request.soru_tipi.value
    
    # Gemini API ile soru üretmeyi dene
    generated_questions = []
    if model:
        try:
            prompt = f"""
            8. sınıf Türkçe dersi, LGS müfredatına uygun olarak '{request.konu}' konusunda, '{request.soru_tipi.value}' türünde, {request.yil} yılı tarzında 1 adet çoktan seçmeli soru üret.
            
            Çıktı SADECE aşağıdaki JSON formatında olmalıdır, başka hiçbir metin ekleme:
            {{
                "soru_metni": "Soru metni buraya",
                "secenekler": ["A) ...", "B) ...", "C) ...", "D) ..."],
                "dogru_cevap": "A) ..."
            }}
            """
            
            # İstenen sayı (3) kadar soru üret
            for _ in range(3):
                response = model.generate_content(prompt)
                try:
                    # JSON temizliği (Markdown backticklerini kaldır)
                    text_response = response.text.strip()
                    if text_response.startswith("```json"):
                        text_response = text_response[7:-3]
                    elif text_response.startswith("```"):
                         text_response = text_response[3:-3]
                    
                    soru_data = json.loads(text_response)
                    generated_questions.append(soru_data)
                except Exception as parse_err:
                    print(f"JSON Parse Hatası: {parse_err} - Yanıt: {response.text}")
                    # Parse hatası olursa döngüye devam et (mock'a düşebilir)
        
        except Exception as e:
            print(f"Gemini API Hatası: {e}")
            # API hatasında mock veriye düş

    # Eğer API'den yeterli soru gelmediyse Mock veriyi kullan
    if len(generated_questions) < 3:
        # Mock veriden tamamla
        topic_questions = MOCK_SORULAR.get(soru_tipi_str, {}).get(request.konu, [])
        if not topic_questions:
             topic_questions = [{
                "soru_metni": f"{request.konu} konusunda henüz özel soru eklenmemiş, ancak sistem çalışıyor! ({request.yil})",
                "secenekler": ["A) Örnek 1", "B) Örnek 2", "C) Örnek 3", "D) Örnek 4"],
                "dogru_cevap": "A) Örnek 1"
            }]
        
        # Eksik kalan kısmı mock ile doldur
        needed = 3 - len(generated_questions)
        if len(topic_questions) >= needed:
            chunk = random.sample(topic_questions, needed) if len(topic_questions) > needed else [random.choice(topic_questions) for _ in range(needed)]
            generated_questions.extend(chunk)
        else:
             generated_questions.extend([random.choice(topic_questions) for _ in range(needed)])


    # SoruResponse objelerine dönüştür
    sorular = []
    for item in generated_questions:
        sorular.append(SoruResponse(
            id=random.randint(1000, 9999),
            soru_metni=item["soru_metni"],
            secenekler=item["secenekler"],
            dogru_cevap=item["dogru_cevap"],
            konu=request.konu,
            yil=request.yil,
            soru_tipi=soru_tipi_str
        ))
    
    return sorular


# ==================== PROFİL ENDPOINT'LERİ ====================

@app.get("/api/profil/bilgiler", response_model=KullaniciBilgiResponse)
async def kullanici_bilgileri(username: str):
    """
    Kullanıcı profil bilgilerini döner
    """
    if users_collection is None:
        return KullaniciBilgiResponse(ad="Misafir", email="", sinif="", avatar_url="/img/user.png")

    user = users_collection.find_one({"username": username})
    if not user:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")
    
    return KullaniciBilgiResponse(
        ad=user.get("username", "Kullanıcı"),
        email=user.get("email", ""),
        sinif="8. Sınıf", # Sabit veya DB'den
        avatar_url="/img/user.png"
    )


@app.get("/api/profil/istatistikler", response_model=ProfilIstatistikResponse)
async def profil_istatistikleri(username: str):
    """
    Kullanıcının tahmin oluşturma istatistiklerini döner
    """
    toplam_tahmin = 0
    favori_konu = "-"
    son_aktivite = "-"
    gunluk_ortalama = 0.0

    if users_collection is not None:
        # Toplam Tahmin
        toplam_tahmin = db.predictions.count_documents({"username": username})
        
        # Favori Konu
        pipeline = [
            {"$match": {"username": username}},
            {"$group": {"_id": "$konu", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 1}
        ]
        result = list(db.predictions.aggregate(pipeline))
        if result:
            favori_konu = result[0]["_id"]

        # Son Aktivite
        last_item = db.predictions.find_one(
            {"username": username}, 
            sort=[("tarih", -1)]
        )
        if last_item:
            # Tarih formatı: 12 Kasım 2024
            ts = last_item["tarih"]
            # Türkçe ay isimleri için basit map
            aylar = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
            son_aktivite = f"{ts.day} {aylar[ts.month-1]} {ts.year}"
        
        # Günlük Ortalama (Basitçe kayıt tarihinden bugüne)
        user = users_collection.find_one({"username": username})
        if user and "created_at" in user:
            days = (datetime.now() - user["created_at"]).days
            if days < 1: days = 1
            gunluk_ortalama = round(toplam_tahmin / days, 1)
        else:
             gunluk_ortalama = float(toplam_tahmin) # Yeni kullanıcı gibi

    return ProfilIstatistikResponse(
        toplam_tahmin=toplam_tahmin,
        favori_konu=favori_konu,
        son_aktivite=son_aktivite,
        gunluk_ortalama=gunluk_ortalama
    )


@app.get("/api/profil/grafik/haftalik", response_model=GrafikVeriResponse)
async def haftalik_grafik(username: str = None):
    # Basit mock (şimdilik) veya gerçek veri eklenebilir
    return GrafikVeriResponse(
        labels=["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"],
        data=[random.randint(0, 10) for _ in range(7)]
    )


@app.get("/api/profil/grafik/dogru-cevaplar", response_model=GrafikVeriResponse)
async def dogru_cevaplar_grafigi(username: str = None):
     # Konu Dağılımı gibi düşünülebilir
    return GrafikVeriResponse(
        labels=["Anlam", "Paragraf", "Sözel M.", "Yazım", "Noktalama"],
        data=[random.randint(5, 20) for _ in range(5)]
    )


@app.get("/api/profil/son-cozulen-sorular", response_model=List[SonCozulenSoruResponse])
async def son_cozulen_sorular(username: str):
    """
    Son oluşturulan tahminleri döner
    """
    recent = []
    if users_collection is not None:
        cursor = db.predictions.find({"username": username}).sort("tarih", -1).limit(10)
        aylar = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
        
        for item in cursor:
            ts = item["tarih"]
            tarih_str = f"{ts.day} {aylar[ts.month-1]} {ts.hour}:{ts.minute:02d}"
            
            recent.append(SonCozulenSoruResponse(
                tarih=tarih_str,
                konu=item["konu"],
                yil=item.get("yil", 2024),
                tur=item["soru_tipi"]
            ))
            
    return recent



# ==================== AI RAPORLAMA ENDPOINT'İ ====================

class AiReportRequest(BaseModel):
    username: str

class AiReportResponse(BaseModel):
    markdown_report: str
    trends: list

@app.post("/api/ai/report", response_model=AiReportResponse)
async def generate_ai_report(request: AiReportRequest):
    """
    Kullanıcının geçmiş verilerini analiz edip Gemini ile rapor oluşturur.
    """
    username = request.username
    
    if users_collection is None:
         # DB yoksa mock rapor
        return AiReportResponse(
            markdown_report="## 🤖 TahminX AI Raporu (Demo)\n\nVeritabanı bağlantısı olmadığı için örnek rapor gösteriliyor.\n\n*   **Güçlü Yönler:** Paragraf sorularında iyisin.\n*   **Gelişim Alanları:** Sözel mantık üzerine eğilmelisin.\n",
            trends=[10, 15, 8, 20, 25]
        )

    # 1. Kullanıcı geçmişini çek
    cursor = db.predictions.find({"username": username}).sort("tarih", -1).limit(50)
    history = list(cursor)
    
    if not history:
        return AiReportResponse(
            markdown_report="## 📉 Veri Yetersiz\n\nHenüz yeterince soru üretmemişsin. AI analizi için biraz daha tahmin yapmalısın! Hemen 'Sana Özel Sorular' sayfasına gidip birkaç soru üret.",
            trends=[]
        )

    # 2. Veriyi özetle
    total_questions = len(history)
    topics = {}
    for item in history:
        t = item.get("konu", "Bilinmiyor")
        topics[t] = topics.get(t, 0) + 1
        
    most_studied = max(topics, key=topics.get) if topics else "Yok"
    
    # 3. Gemini Prompt Hazırla
    prompt = f"""
    Sen 'TahminX' adında LGS (Liselere Geçiş Sınavı) öğrencilerine koçluk yapan bir yapay zekasın.
    Aşağıdaki öğrenci verilerine göre ona motive edici, stratejik ve kişiselleştirilmiş bir çalışma raporu hazırla.
    Raporu Markdown formatında yaz. Başlıklar, maddeler ve emojiler kullan.

    **Öğrenci Verileri:**
    - Toplam Üretilen Soru: {total_questions}
    - En Çok Çalışılan Konu: {most_studied}
    - Konu Dağılımı: {json.dumps(topics, ensure_ascii=False)}
    - Son Aktiviteler (Yeniden eskiye): {[h.get('konu') for h in history[:5]]}

    **İstenen Rapor Formatı:**
    1. ** Genel Bakış:** Öğrencinin durumunu özetle (Motive edici ton).
    2. **📊 Güçlü ve Zayıf Yönler:** Hangi konulara çok yüklenmiş, hangilerini ihmal etmiş?
    3. **🧭 Gelecek Rotası:** Önümüzdeki 1 hafta için sınav stratejisi ne olmalı? Hangi konulara yönelmeli?
    4. **💡 TahminX Tavsiyesi:** Kısa ve net bir başarı ipucu.

    Lütfen samimi, koç vari ve profesyonel bir dil kullan. Türkçe cevap ver.
    """

    try:
        # Gemini'yi çağır
        model = genai.GenerativeModel('gemini-flash-latest')
        response = model.generate_content(prompt)
        report_text = response.text
    except Exception as e:
        print(f"Gemini Hatası: {e}")
        # Fallback: API hatası veya kota dolumu durumunda Mock Rapor dön
        report_text = f"""
## 🤖 TahminX AI Raporu (Simülasyon)

**⚠️ Bilgi:** Google Gemini AI günlük kullanım kotanız dolduğu için şu an **örnek bir analiz** görmektesiniz. Kota yenilendiğinde gerçek verileriniz analiz edilecektir.

### 1. Genel Bakış
Harika bir başlangıç yapmışsın! 🚀 Paragraf sorularına olan ilgin takdire şayan. Ancak genel başarını artırmak için sadece sevdiğin konulara değil, seni zorlayan konulara da odaklanmalısın.

### 2. 📊 Güçlü ve Zayıf Yönler
*   **Güçlü:** {most_studied} konusunda oldukça fazla pratik yapmışsın. Bu konuda artık ustalaşma yolundasın.
*   **Gelişim Alanı:** Diğer konulara (örneğin Yazım Kuralları veya Sözel Mantık) daha az vakit ayırmışsın. Dengeyi kurmalıyız.

### 3. 🧭 Gelecek Rotası
*   **Pazartesi:** Hiç çözmediğin bir konudan 10 soru çöz.
*   **Çarşamba:** {most_studied} konusundan zorluk seviyesi yüksek 5 soru ile kendini sına.
*   **Haftasonu:** Genel bir deneme sınavı (tüm konulardan karışık) yap.

### 4. 💡 TahminX Tavsiyesi
> "En büyük başarı, en çok zorlandığın soruyu çözdüğün an başlar." 🌟
        """

    # Trend verisi (Basitçe son 7 aktivite veya gruplandırma - şimdilik mock trend)
    # Gerçekte tarihe göre gruplayıp sayıları dönebiliriz.
    trend_data = [topics.get(k, 0) for k in list(topics.keys())[:5]] 

    return AiReportResponse(
        markdown_report=report_text,
        trends=trend_data
    )


# ==================== HEALTH CHECK ====================


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}



# Statik dosyaları en sonda sun ki API route'ları ezilmesin
app.mount("/", StaticFiles(directory="static", html=True), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

