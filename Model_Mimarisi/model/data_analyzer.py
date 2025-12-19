"""
LGS Türkçe Soru Tahminleme - Veri Analiz Modülü
Geçmiş LGS sorularından pattern çıkarma ve istatistiksel analiz
"""

import json
from pathlib import Path
from collections import Counter, defaultdict
from typing import Dict, List, Any, Optional
import re


class DataAnalyzer:
    """
    LGS Türkçe soruları üzerinde analiz yapan sınıf.
    Pattern çıkarma, kategori dağılımı, keyword analizi yapar.
    """
    
    def __init__(self, data_path: str = None):
        """
        Args:
            data_path: JSON veri dosyasının yolu
        """
        self.data_path = data_path
        self.data = None
        self.analysis_cache = {}
        
        if data_path:
            self.load_data(data_path)
    
    def load_data(self, data_path: str) -> bool:
        """
        JSON veri dosyasını yükler.
        
        Args:
            data_path: JSON dosyası yolu
            
        Returns:
            bool: Başarılı ise True
        """
        try:
            path = Path(data_path)
            if not path.exists():
                raise FileNotFoundError(f"Veri dosyası bulunamadı: {data_path}")
            
            with open(path, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            
            self.data_path = data_path
            self.analysis_cache = {}  # Cache'i temizle
            return True
        except Exception as e:
            print(f"Veri yükleme hatası: {e}")
            return False
    
    def get_total_questions(self) -> int:
        """Toplam soru sayısını döndürür."""
        if not self.data:
            return 0
        return len(self.data.get('Ticket_ID', []))
    
    def get_category_distribution(self) -> Dict[str, int]:
        """
        Kategori dağılımını hesaplar.
        
        Returns:
            Dict: Kategori -> Soru sayısı
        """
        if 'category_dist' in self.analysis_cache:
            return self.analysis_cache['category_dist']
        
        if not self.data:
            return {}
        
        categories = self.data.get('Kategori', [])
        distribution = dict(Counter(categories))
        
        self.analysis_cache['category_dist'] = distribution
        return distribution
    
    def get_subcategory_distribution(self) -> Dict[str, Dict[str, int]]:
        """
        Alt kategori dağılımını hesaplar.
        
        Returns:
            Dict: Kategori -> {Alt Kategori -> Sayı}
        """
        if 'subcategory_dist' in self.analysis_cache:
            return self.analysis_cache['subcategory_dist']
        
        if not self.data:
            return {}
        
        categories = self.data.get('Kategori', [])
        subcategories = self.data.get('Alt Başlık', [])
        
        distribution = defaultdict(lambda: defaultdict(int))
        
        for cat, subcat in zip(categories, subcategories):
            distribution[cat][subcat] += 1
        
        # defaultdict'i normal dict'e çevir
        result = {k: dict(v) for k, v in distribution.items()}
        
        self.analysis_cache['subcategory_dist'] = result
        return result
    
    def get_year_distribution(self) -> Dict[str, int]:
        """
        Yıllara göre soru dağılımını hesaplar.
        
        Returns:
            Dict: Yıl -> Soru sayısı
        """
        if 'year_dist' in self.analysis_cache:
            return self.analysis_cache['year_dist']
        
        if not self.data:
            return {}
        
        ticket_ids = self.data.get('Ticket_ID', [])
        years = []
        
        for tid in ticket_ids:
            # LGS-2018-C-001 veya MEB-C-001 formatı
            if tid.startswith('LGS-'):
                year = tid.split('-')[1]
                years.append(year)
            else:
                years.append('MEB')
        
        distribution = dict(Counter(years))
        
        self.analysis_cache['year_dist'] = distribution
        return distribution
    
    def get_keyword_frequency(self, top_n: int = 50) -> List[tuple]:
        """
        En sık kullanılan anahtar kelimeleri döndürür.
        
        Args:
            top_n: En sık kaç kelime döndürüleceği
            
        Returns:
            List: (kelime, frekans) tuple listesi
        """
        if not self.data:
            return []
        
        keywords = self.data.get('Keywords', [])
        all_keywords = []
        
        for kw_list in keywords:
            if isinstance(kw_list, list):
                all_keywords.extend(kw_list)
        
        frequency = Counter(all_keywords)
        return frequency.most_common(top_n)
    
    def get_questions_by_category(self, category: str) -> List[Dict]:
        """
        Belirli bir kategorideki soruları döndürür.
        
        Args:
            category: Kategori adı
            
        Returns:
            List: Soru dictlerinin listesi
        """
        if not self.data:
            return []
        
        questions = []
        categories = self.data.get('Kategori', [])
        
        for i, cat in enumerate(categories):
            if cat == category:
                question = self._get_question_by_index(i)
                if question:
                    questions.append(question)
        
        return questions
    
    def get_questions_by_subcategory(self, subcategory: str) -> List[Dict]:
        """
        Belirli bir alt kategorideki soruları döndürür.
        
        Args:
            subcategory: Alt kategori adı
            
        Returns:
            List: Soru dictlerinin listesi
        """
        if not self.data:
            return []
        
        questions = []
        subcategories = self.data.get('Alt Başlık', [])
        
        for i, subcat in enumerate(subcategories):
            if subcat == subcategory:
                question = self._get_question_by_index(i)
                if question:
                    questions.append(question)
        
        return questions
    
    def _get_question_by_index(self, index: int) -> Optional[Dict]:
        """
        Belirli indeksteki soruyu dict olarak döndürür.
        
        Args:
            index: Soru indeksi
            
        Returns:
            Dict veya None
        """
        if not self.data:
            return None
        
        try:
            return {
                'ticket_id': self.data['Ticket_ID'][index],
                'kategori': self.data['Kategori'][index],
                'alt_baslik': self.data['Alt Başlık'][index],
                'metin': self.data['Metinler'][index],
                'soru_koku': self.data['Soru Kökleri'][index],
                'cevap': self.data['Cevaplar'][index],
                'keywords': self.data['Keywords'][index]
            }
        except (IndexError, KeyError):
            return None
    
    def get_pattern_analysis(self) -> Dict[str, Any]:
        """
        Soru kalıplarını analiz eder.
        
        Returns:
            Dict: Pattern analiz sonuçları
        """
        if 'pattern_analysis' in self.analysis_cache:
            return self.analysis_cache['pattern_analysis']
        
        if not self.data:
            return {}
        
        soru_kokleri = self.data.get('Soru Kökleri', [])
        
        # Soru kalıpları
        patterns = {
            'hangisi': 0,
            'aşağıdakilerden': 0,
            'çıkarılabilir': 0,
            'çıkarılamaz': 0,
            'anlam': 0,
            'düşünce': 0,
            'yargı': 0,
            'tamamlama': 0,
            'sıralama': 0,
            'boşluk_doldurma': 0
        }
        
        for soru in soru_kokleri:
            soru_lower = soru.lower()
            
            if 'hangisi' in soru_lower:
                patterns['hangisi'] += 1
            if 'aşağıdaki' in soru_lower:
                patterns['aşağıdakilerden'] += 1
            if 'çıkarılabilir' in soru_lower or 'ulaşılır' in soru_lower:
                patterns['çıkarılabilir'] += 1
            if 'çıkarılamaz' in soru_lower or 'ulaşılamaz' in soru_lower:
                patterns['çıkarılamaz'] += 1
            if 'anlam' in soru_lower:
                patterns['anlam'] += 1
            if 'düşünce' in soru_lower:
                patterns['düşünce'] += 1
            if 'yargı' in soru_lower:
                patterns['yargı'] += 1
            if 'tamamla' in soru_lower:
                patterns['tamamlama'] += 1
            if 'sırala' in soru_lower:
                patterns['sıralama'] += 1
            if 'boş' in soru_lower and 'yer' in soru_lower:
                patterns['boşluk_doldurma'] += 1
        
        analysis = {
            'total_questions': self.get_total_questions(),
            'question_patterns': patterns,
            'category_distribution': self.get_category_distribution(),
            'year_distribution': self.get_year_distribution(),
            'top_keywords': self.get_keyword_frequency(30)
        }
        
        self.analysis_cache['pattern_analysis'] = analysis
        return analysis
    
    def get_sample_questions(self, category: str = None, n: int = 5) -> List[Dict]:
        """
        Örnek sorular döndürür (few-shot learning için).
        
        Args:
            category: Opsiyonel kategori filtresi
            n: Döndürülecek soru sayısı
            
        Returns:
            List: Örnek sorular
        """
        if not self.data:
            return []
        
        if category:
            questions = self.get_questions_by_category(category)
        else:
            questions = [
                self._get_question_by_index(i) 
                for i in range(self.get_total_questions())
            ]
            questions = [q for q in questions if q]
        
        # Her kategoriden dengeli örnekleme yap
        import random
        random.seed(42)  # Tekrarlanabilirlik için
        
        if len(questions) <= n:
            return questions
        
        return random.sample(questions, n)
    
    def get_prediction_context(self, category: str = None) -> Dict[str, Any]:
        """
        2026 LGS tahminlemesi için bağlam oluşturur.
        
        Args:
            category: Opsiyonel kategori filtresi
            
        Returns:
            Dict: Tahminleme bağlamı
        """
        pattern_analysis = self.get_pattern_analysis()
        
        context = {
            'total_analyzed_questions': pattern_analysis['total_questions'],
            'category_trends': pattern_analysis['category_distribution'],
            'question_patterns': pattern_analysis['question_patterns'],
            'popular_topics': pattern_analysis['top_keywords'][:15],
            'sample_questions': self.get_sample_questions(category, n=10),
            'years_covered': list(pattern_analysis['year_distribution'].keys())
        }
        
        # Kategori bazlı trend analizi
        if category:
            context['category_specific'] = {
                'subcategories': self.get_subcategory_distribution().get(category, {}),
                'sample_count': len(self.get_questions_by_category(category))
            }
        
        return context
    
    def export_analysis_report(self) -> Dict[str, Any]:
        """
        Tam analiz raporu oluşturur.
        
        Returns:
            Dict: Detaylı analiz raporu
        """
        return {
            'summary': {
                'total_questions': self.get_total_questions(),
                'categories': len(self.get_category_distribution()),
                'years': len(self.get_year_distribution())
            },
            'category_distribution': self.get_category_distribution(),
            'subcategory_distribution': self.get_subcategory_distribution(),
            'year_distribution': self.get_year_distribution(),
            'pattern_analysis': self.get_pattern_analysis(),
            'top_keywords': self.get_keyword_frequency(50)
        }

