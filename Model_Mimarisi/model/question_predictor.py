"""
LGS Türkçe Soru Tahminleme - Hibrit Tahminleme Modülü
Veri analizi + Gemini API birleşik sistem
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

from .data_analyzer import DataAnalyzer
from .gemini_client import GeminiClient


class QuestionPredictor:
    """
    Hibrit soru tahminleme sistemi.
    Geçmiş LGS verilerini analiz eder ve Gemini ile yeni sorular üretir.
    """
    
    # Desteklenen kategoriler
    SUPPORTED_CATEGORIES = [
        "Paragrafta Anlam",
        "Cümlede Anlam", 
        "Sözcükte Anlam",
        "Söz Öbeğinde Anlam",
        "Paragrafta Yapı",
        "Şiirde Anlam"
    ]
    
    DIFFICULTY_LEVELS = ["kolay", "orta", "zor"]
    
    def __init__(self, data_path: str, api_key: str, model_name: str = "models/gemini-1.5-flash"):
        """
        Args:
            data_path: Eğitim verisi JSON dosyasının yolu
            api_key: Gemini API anahtarı
            model_name: Kullanılacak Gemini modeli
        """
        self.data_analyzer = DataAnalyzer(data_path)
        self.gemini_client = GeminiClient(api_key, model_name)
        self.generated_questions = []
        self.prediction_history = []
    
    def get_model_status(self) -> Dict[str, Any]:
        """
        Model durumunu döndürür.
        
        Returns:
            Dict: Model durum bilgileri
        """
        return {
            "status": "active",
            "total_training_questions": self.data_analyzer.get_total_questions(),
            "supported_categories": self.SUPPORTED_CATEGORIES,
            "difficulty_levels": self.DIFFICULTY_LEVELS,
            "generated_questions_count": len(self.generated_questions),
            "data_analysis": self.data_analyzer.get_pattern_analysis()
        }
    
    def predict_questions(
        self,
        category: str = None,
        subcategory: str = None,
        count: int = 5,
        difficulty: str = "orta"
    ) -> Dict[str, Any]:
        """
        2026 LGS için soru tahminlemesi yapar.
        
        Args:
            category: Ana kategori (None ise rastgele)
            subcategory: Alt kategori (opsiyonel)
            count: Üretilecek soru sayısı (1-10)
            difficulty: Zorluk seviyesi
            
        Returns:
            Dict: Tahminleme sonuçları
        """
        # Validasyon
        if count < 1 or count > 10:
            return {"error": "Soru sayısı 1-10 arasında olmalıdır."}
        
        if difficulty.lower() not in self.DIFFICULTY_LEVELS:
            return {"error": f"Geçersiz zorluk seviyesi. Seçenekler: {self.DIFFICULTY_LEVELS}"}
        
        if category and category not in self.SUPPORTED_CATEGORIES:
            return {
                "error": f"Geçersiz kategori. Desteklenen kategoriler: {self.SUPPORTED_CATEGORIES}"
            }
        
        # Kategori belirtilmemişse en popüler kategoriyi seç
        if not category:
            cat_dist = self.data_analyzer.get_category_distribution()
            category = max(cat_dist, key=cat_dist.get) if cat_dist else "Paragrafta Anlam"
        
        # Tahminleme bağlamını oluştur
        context = self.data_analyzer.get_prediction_context(category)
        
        # Gemini ile soru üret
        questions = self.gemini_client.generate_questions(
            context=context,
            category=category,
            subcategory=subcategory,
            count=count,
            difficulty=difficulty
        )
        
        # Sonuçları kaydet
        prediction_result = {
            "timestamp": datetime.now().isoformat(),
            "request": {
                "category": category,
                "subcategory": subcategory,
                "count": count,
                "difficulty": difficulty
            },
            "generated_questions": questions,
            "success": len(questions) > 0,
            "analysis_context": {
                "total_training_data": context.get('total_analyzed_questions', 0),
                "category_sample_count": len(context.get('sample_questions', [])),
                "years_analyzed": context.get('years_covered', [])
            }
        }
        
        self.generated_questions.extend(questions)
        self.prediction_history.append(prediction_result)
        
        return prediction_result
    
    def get_2026_predictions(self) -> Dict[str, Any]:
        """
        2026 LGS için genel trend tahminleri döndürür.
        
        Returns:
            Dict: Trend tahminleri ve öneriler
        """
        context = self.data_analyzer.get_prediction_context()
        trends = self.gemini_client.predict_2026_trends(context)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "data_analysis_summary": self.data_analyzer.export_analysis_report()['summary'],
            "trend_predictions": trends,
            "category_distribution": self.data_analyzer.get_category_distribution(),
            "question_patterns": context.get('question_patterns', {})
        }
    
    def analyze_question(self, question_text: str) -> Dict[str, Any]:
        """
        Bir soruyu analiz eder.
        
        Args:
            question_text: Analiz edilecek soru
            
        Returns:
            Dict: Analiz sonuçları
        """
        # Türkçe dersi kontrolü
        if not self.gemini_client.is_turkish_related(question_text):
            return {
                "error": "Bu soru Türkçe dersiyle ilgili görünmüyor.",
                "message": "Bu sistem sadece LGS Türkçe soruları için tasarlanmıştır."
            }
        
        analysis = self.gemini_client.analyze_question(question_text)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "question": question_text[:500] + "..." if len(question_text) > 500 else question_text,
            "analysis": analysis
        }
    
    def get_category_statistics(self) -> Dict[str, Any]:
        """
        Kategori bazlı detaylı istatistikler döndürür.
        
        Returns:
            Dict: Kategori istatistikleri
        """
        return {
            "category_distribution": self.data_analyzer.get_category_distribution(),
            "subcategory_distribution": self.data_analyzer.get_subcategory_distribution(),
            "year_distribution": self.data_analyzer.get_year_distribution(),
            "top_keywords": self.data_analyzer.get_keyword_frequency(30)
        }
    
    def get_sample_questions_by_category(
        self, 
        category: str, 
        count: int = 5
    ) -> List[Dict]:
        """
        Belirli bir kategoriden örnek sorular döndürür.
        
        Args:
            category: Kategori adı
            count: Döndürülecek soru sayısı
            
        Returns:
            List: Örnek sorular
        """
        if category not in self.SUPPORTED_CATEGORIES:
            return []
        
        return self.data_analyzer.get_sample_questions(category, count)
    
    def export_generated_questions(self, file_path: str = None) -> str:
        """
        Üretilen soruları JSON dosyasına kaydeder.
        
        Args:
            file_path: Kayıt dosyası yolu (opsiyonel)
            
        Returns:
            str: Kayıt dosyası yolu
        """
        if not file_path:
            file_path = f"generated_questions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        export_data = {
            "export_timestamp": datetime.now().isoformat(),
            "total_questions": len(self.generated_questions),
            "questions": self.generated_questions
        }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
        
        return file_path
    
    def get_prediction_history(self) -> List[Dict]:
        """
        Tahminleme geçmişini döndürür.
        
        Returns:
            List: Tahminleme geçmişi
        """
        return self.prediction_history
    
    def clear_generated_questions(self):
        """Üretilen soruları temizler."""
        self.generated_questions = []
        self.prediction_history = []
    
    def get_subcategories(self, category: str) -> List[str]:
        """
        Bir kategorinin alt kategorilerini döndürür.
        
        Args:
            category: Ana kategori
            
        Returns:
            List: Alt kategoriler
        """
        subcat_dist = self.data_analyzer.get_subcategory_distribution()
        return list(subcat_dist.get(category, {}).keys())

