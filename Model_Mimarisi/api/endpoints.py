"""
LGS Türkçe Soru Tahminleme - REST API Endpoints
FastAPI tabanlı web API
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
import os
import sys
from pathlib import Path

# Model modüllerini import et
sys.path.insert(0, str(Path(__file__).parent.parent))
from model.question_predictor import QuestionPredictor

# Konfigürasyon
BASE_DIR = Path(__file__).parent.parent
DATA_FILE = BASE_DIR / "data.json"

# Ortam değişkenlerinden API key al
from dotenv import load_dotenv
load_dotenv(BASE_DIR / ".env")
load_dotenv(BASE_DIR.parent / ".env")

GEMINI_API_KEY = os.getenv("Gemini_API_Key", "")

# FastAPI uygulaması
app = FastAPI(
    title="LGS Türkçe Soru Tahminleme API",
    description="""
    ## 🎓 LGS Türkçe Soru Tahminleme Modeli
    
    Bu API, geçmiş LGS Türkçe sorularını analiz ederek 2026 sınavı için 
    yeni soru tahminleri üretir.
    
    ### Özellikler:
    - 📊 Veri analizi ve pattern çıkarma
    - 🤖 Gemini AI ile soru üretimi
    - 📈 Trend tahminleri
    - 🔍 Soru analizi
    
    ### Kategoriler:
    - Paragrafta Anlam
    - Cümlede Anlam
    - Sözcükte Anlam
    - Söz Öbeğinde Anlam
    - Paragrafta Yapı
    - Şiirde Anlam
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS ayarları (web sitesi entegrasyonu için)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production'da bunu kısıtlayın
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router
from fastapi import APIRouter
router = APIRouter(prefix="/api/v1", tags=["LGS Türkçe"])

# Global predictor instance
predictor: Optional[QuestionPredictor] = None


def get_predictor() -> QuestionPredictor:
    """Predictor instance döndürür, yoksa oluşturur."""
    global predictor
    
    if predictor is None:
        if not GEMINI_API_KEY or GEMINI_API_KEY == "BURAYA_API_ANAHTARINIZI_GIRIN":
            raise HTTPException(
                status_code=500,
                detail="API anahtarı yapılandırılmamış. .env dosyasında Gemini_API_Key değerini ayarlayın."
            )
        
        if not DATA_FILE.exists():
            raise HTTPException(
                status_code=500,
                detail=f"Veri dosyası bulunamadı: {DATA_FILE}"
            )
        
        predictor = QuestionPredictor(
            data_path=str(DATA_FILE),
            api_key=GEMINI_API_KEY
        )
    
    return predictor


# ==================== REQUEST/RESPONSE MODELLERİ ====================

class QuestionGenerationRequest(BaseModel):
    """Soru üretme isteği modeli"""
    category: Optional[str] = Field(
        None, 
        description="Ana kategori (Paragrafta Anlam, Cümlede Anlam vb.)"
    )
    subcategory: Optional[str] = Field(
        None,
        description="Alt kategori"
    )
    count: int = Field(
        5,
        ge=1,
        le=10,
        description="Üretilecek soru sayısı (1-10)"
    )
    difficulty: str = Field(
        "orta",
        description="Zorluk seviyesi: kolay, orta, zor"
    )


class QuestionAnalysisRequest(BaseModel):
    """Soru analizi isteği modeli"""
    question_text: str = Field(
        ...,
        min_length=10,
        description="Analiz edilecek soru metni"
    )


class GeneratedQuestion(BaseModel):
    """Üretilen soru modeli"""
    soru_no: int
    kategori: str
    alt_baslik: str
    zorluk: str
    metin: Optional[str]
    soru: str
    secenekler: dict
    dogru_cevap: str
    aciklama: str


class APIResponse(BaseModel):
    """Standart API yanıt modeli"""
    success: bool
    message: str
    data: Optional[dict] = None


# ==================== API ENDPOINTS ====================

@router.get("/", response_model=APIResponse)
async def root():
    """API durumunu kontrol eder."""
    return APIResponse(
        success=True,
        message="LGS Türkçe Soru Tahminleme API aktif",
        data={"version": "1.0.0"}
    )


@router.get("/status")
async def get_status():
    """Model durumunu döndürür."""
    try:
        pred = get_predictor()
        status = pred.get_model_status()
        return {
            "success": True,
            "data": status
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        return {"success": False, "error": str(e)}


@router.get("/categories")
async def get_categories():
    """Desteklenen kategorileri döndürür."""
    try:
        pred = get_predictor()
        stats = pred.get_category_statistics()
        
        return {
            "success": True,
            "data": {
                "supported_categories": QuestionPredictor.SUPPORTED_CATEGORIES,
                "category_distribution": stats["category_distribution"],
                "subcategory_distribution": stats["subcategory_distribution"]
            }
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        return {"success": False, "error": str(e)}


@router.get("/categories/{category}/subcategories")
async def get_subcategories(category: str):
    """Bir kategorinin alt kategorilerini döndürür."""
    try:
        pred = get_predictor()
        subcategories = pred.get_subcategories(category)
        
        if not subcategories:
            return {
                "success": False,
                "error": f"Kategori bulunamadı: {category}"
            }
        
        return {
            "success": True,
            "data": {
                "category": category,
                "subcategories": subcategories
            }
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        return {"success": False, "error": str(e)}


@router.post("/generate")
async def generate_questions(request: QuestionGenerationRequest):
    """
    Yeni LGS Türkçe soruları üretir.
    
    2026 LGS sınavı için tahmin edilen sorular üretir.
    """
    try:
        pred = get_predictor()
        result = pred.predict_questions(
            category=request.category,
            subcategory=request.subcategory,
            count=request.count,
            difficulty=request.difficulty
        )
        
        if "error" in result:
            return {"success": False, "error": result["error"]}
        
        return {
            "success": True,
            "data": result
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        return {"success": False, "error": str(e)}


@router.get("/predict/trends")
async def get_trend_predictions():
    """2026 LGS için trend tahminlerini döndürür."""
    try:
        pred = get_predictor()
        predictions = pred.get_2026_predictions()
        
        return {
            "success": True,
            "data": predictions
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        return {"success": False, "error": str(e)}


@router.post("/analyze")
async def analyze_question(request: QuestionAnalysisRequest):
    """Verilen soruyu analiz eder."""
    try:
        pred = get_predictor()
        analysis = pred.analyze_question(request.question_text)
        
        if "error" in analysis:
            return {"success": False, "error": analysis["error"]}
        
        return {
            "success": True,
            "data": analysis
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        return {"success": False, "error": str(e)}


@router.get("/statistics")
async def get_statistics():
    """Veri istatistiklerini döndürür."""
    try:
        pred = get_predictor()
        stats = pred.get_category_statistics()
        
        return {
            "success": True,
            "data": stats
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        return {"success": False, "error": str(e)}


@router.get("/sample/{category}")
async def get_sample_questions(
    category: str,
    count: int = Query(5, ge=1, le=20, description="Örnek soru sayısı")
):
    """Belirli bir kategoriden örnek sorular döndürür."""
    try:
        pred = get_predictor()
        samples = pred.get_sample_questions_by_category(category, count)
        
        if not samples:
            return {
                "success": False,
                "error": f"Kategori bulunamadı veya örnek yok: {category}"
            }
        
        return {
            "success": True,
            "data": {
                "category": category,
                "count": len(samples),
                "questions": samples
            }
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        return {"success": False, "error": str(e)}


@router.get("/history")
async def get_generation_history():
    """Üretim geçmişini döndürür."""
    try:
        pred = get_predictor()
        history = pred.get_prediction_history()
        
        return {
            "success": True,
            "data": {
                "total_predictions": len(history),
                "history": history[-10:]  # Son 10 kayıt
            }
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        return {"success": False, "error": str(e)}


@router.delete("/clear")
async def clear_generated():
    """Üretilen soruları temizler."""
    try:
        pred = get_predictor()
        pred.clear_generated_questions()
        
        return {
            "success": True,
            "message": "Üretilen sorular temizlendi"
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        return {"success": False, "error": str(e)}


# Router'ı uygulamaya ekle
app.include_router(router)


# Ana sayfa redirect
@app.get("/")
async def main_redirect():
    """Ana sayfadan API docs'a yönlendir."""
    return {
        "message": "LGS Türkçe Soru Tahminleme API",
        "docs": "/docs",
        "api_base": "/api/v1"
    }


# Hata yönetimi
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Sunucu hatası",
            "detail": str(exc)
        }
    )

