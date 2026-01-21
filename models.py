"""
Pydantic modelleri - API request/response şemaları
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class SoruTipi(str, Enum):
    """Soru tipi enum"""
    CUMLEDE = "cumlede"
    PARAGRAFTA = "paragrafta"


class SoruOlusturRequest(BaseModel):
    """Soru oluşturma isteği modeli"""
    konu: str = Field(..., description="Seçilen konu adı")
    yil: int = Field(..., ge=2020, le=2025, description="Yıl bilgisi (2020-2025)")
    soru_tipi: SoruTipi = Field(..., description="Soru tipi: cumlede veya paragrafta")
    username: Optional[str] = Field(None, description="İsteği yapan kullanıcı (opsiyonel)")

    class Config:
        json_schema_extra = {
            "example": {
                "konu": "Anlam İlişkileri",
                "yil": 2024,
                "soru_tipi": "cumlede",
                "username": "gokceyavuz"
            }
        }


class SoruResponse(BaseModel):
    """Soru response modeli"""
    id: int
    soru_metni: str
    secenekler: List[str]
    dogru_cevap: str
    konu: str
    yil: int
    soru_tipi: str

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "soru_metni": "Aşağıdaki cümlede hangi anlam ilişkisi vardır?",
                "secenekler": ["A) Neden-Sonuç", "B) Amaç-Sonuç", "C) Koşul-Sonuç", "D) Karşılaştırma"],
                "dogru_cevap": "A) Neden-Sonuç",
                "konu": "Anlam İlişkileri",
                "yil": 2024,
                "soru_tipi": "cumlede"
            }
        }


class ProfilIstatistikResponse(BaseModel):
    """Profil istatistikleri response modeli"""
    toplam_tahmin: int
    favori_konu: str
    son_aktivite: str
    gunluk_ortalama: float

    class Config:
        json_schema_extra = {
            "example": {
                "toplam_tahmin": 42,
                "favori_konu": "Anlam İlişkileri",
                "son_aktivite": "12 Kasım 2024",
                "gunluk_ortalama": 2.5
            }
        }


class GrafikVeriResponse(BaseModel):
    """Grafik verisi response modeli"""
    labels: List[str]
    data: List[int]

    class Config:
        json_schema_extra = {
            "example": {
                "labels": ["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"],
                "data": [12, 9, 7, 14, 18, 5, 8]
            }
        }


class SonCozulenSoruResponse(BaseModel):
    """Son aktivite response modeli"""
    tarih: str
    konu: str
    yil: int
    tur: str

    class Config:
        json_schema_extra = {
            "example": {
                "tarih": "12 Kasım 14:30",
                "konu": "Anlam İlişkileri",
                "yil": 2023,
                "tur": "Cümlede"
            }
        }


class KonularResponse(BaseModel):
    """Konular listesi response modeli"""
    konular: List[str]
    soru_tipi: str

    class Config:
        json_schema_extra = {
            "example": {
                "konular": ["Anlam İlişkileri", "Neden - Sonuç", "Amaç - Sonuç"],
                "soru_tipi": "cumlede"
            }
        }


class KullaniciBilgiResponse(BaseModel):
    """Kullanıcı bilgileri response modeli"""
    ad: str
    email: str
    sinif: str
    avatar_url: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "ad": "Gökçe Yavuz",
                "email": "gokceeyavuz@example.com",
                "sinif": "8. Sınıf",
                "avatar_url": "/img/user.png"
            }
        }

