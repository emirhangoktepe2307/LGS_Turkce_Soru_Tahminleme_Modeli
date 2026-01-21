"""
LGS Türkçe Soru Tahminleme - Gemini API Client
Google Gemini API entegrasyonu ve soru üretimi
"""

import json
import re
from typing import Dict, List, Any, Optional
import google.generativeai as genai


class GeminiClient:
    """
    Google Gemini API ile iletişim kuran sınıf.
    LGS Türkçe soruları üretir ve analiz eder.
    """
    
    def __init__(self, api_key: str, model_name: str = "models/gemini-1.5-flash"):
        """
        Args:
            api_key: Gemini API anahtarı
            model_name: Kullanılacak model adı
        """
        self.api_key = api_key
        self.model_name = model_name
        self.model = None
        self._configure_api()
    
    def _configure_api(self):
        """API yapılandırmasını yapar."""
        genai.configure(api_key=self.api_key)
        
        # Model yapılandırması
        generation_config = {
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
        }
        
        # Güvenlik ayarları (eğitim içeriği için uygun)
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]
        
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            generation_config=generation_config,
            safety_settings=safety_settings
        )
    
    def generate_questions(
        self, 
        context: Dict[str, Any],
        category: str,
        subcategory: str = None,
        count: int = 5,
        difficulty: str = "orta"
    ) -> List[Dict]:
        """
        Verilen bağlama göre yeni LGS Türkçe soruları üretir.
        
        Args:
            context: Veri analizi bağlamı (pattern'lar, örnekler)
            category: Ana kategori (Paragrafta Anlam, Cümlede Anlam vb.)
            subcategory: Alt kategori (opsiyonel)
            count: Üretilecek soru sayısı
            difficulty: Zorluk seviyesi (kolay, orta, zor)
            
        Returns:
            List[Dict]: Üretilen sorular
        """
        prompt = self._build_generation_prompt(
            context, category, subcategory, count, difficulty
        )
        
        try:
            response = self.model.generate_content(prompt)
            questions = self._parse_generated_questions(response.text)
            return questions
        except Exception as e:
            print(f"Soru üretme hatası: {e}")
            return []
    
    def _build_generation_prompt(
        self,
        context: Dict[str, Any],
        category: str,
        subcategory: str,
        count: int,
        difficulty: str
    ) -> str:
        """Soru üretimi için prompt oluşturur."""
        
        # Örnek soruları formatla
        sample_questions = context.get('sample_questions', [])
        examples_text = self._format_sample_questions(sample_questions[:5])
        
        # Trend bilgilerini formatla
        patterns = context.get('question_patterns', {})
        popular_topics = context.get('popular_topics', [])
        
        prompt = f"""Sen bir LGS (Liselere Geçiş Sınavı) Türkçe dersi uzmanısın ve 2026 LGS sınavı için soru tahminlemesi yapıyorsun.

## VERİ ANALİZİ SONUÇLARI

### Analiz Edilen Toplam Soru: {context.get('total_analyzed_questions', 0)}
### Kapsanan Yıllar: {', '.join(context.get('years_covered', []))}

### Soru Kalıpları Dağılımı:
{json.dumps(patterns, ensure_ascii=False, indent=2)}

### En Popüler Konular:
{', '.join([f"{kw[0]} ({kw[1]})" for kw in popular_topics[:10]])}

## ÖRNEK SORULAR (Geçmiş LGS'lerden)
{examples_text}

## GÖREV

**Kategori:** {category}
**Alt Kategori:** {subcategory if subcategory else "Genel"}
**Zorluk:** {difficulty.capitalize()}
**Üretilecek Soru Sayısı:** {count}

2026 LGS sınavında çıkabilecek {count} adet özgün Türkçe sorusu üret.

## KURALLAR
1. Sorular LGS formatında 4 seçenekli (A, B, C, D) olmalı
2. Her sorunun TEK bir doğru cevabı olmalı
3. Sorular {difficulty} zorluk seviyesine uygun olmalı
4. Üretilen sorular özgün olmalı, örnek sorulardan KOPYALANMAMALI
5. Soru metni yeterli uzunlukta ve anlaşılır olmalı
6. Şıklar mantıklı ve birbirine yakın güçlükte olmalı

## ÇIKTI FORMATI (JSON)

```json
[
  {{
    "soru_no": 1,
    "kategori": "{category}",
    "alt_baslik": "{subcategory if subcategory else category}",
    "zorluk": "{difficulty}",
    "metin": "Soru ile ilgili okuma metni veya paragraf (varsa)",
    "soru": "Soru kökü metni",
    "secenekler": {{
      "A": "A şıkkı",
      "B": "B şıkkı", 
      "C": "C şıkkı",
      "D": "D şıkkı"
    }},
    "dogru_cevap": "A/B/C/D",
    "aciklama": "Doğru cevabın detaylı açıklaması"
  }}
]
```

Lütfen SADECE JSON formatında yanıt ver, başka açıklama ekleme.
"""
        return prompt
    
    def _format_sample_questions(self, questions: List[Dict]) -> str:
        """Örnek soruları okunabilir formata çevirir."""
        if not questions:
            return "Örnek soru bulunamadı."
        
        formatted = []
        for i, q in enumerate(questions, 1):
            formatted.append(f"""
### Örnek {i} ({q.get('kategori', 'Bilinmiyor')} - {q.get('alt_baslik', '')})
**Metin:** {q.get('metin', '')[:500]}...
**Soru:** {q.get('soru_koku', '')}
**Cevap:** {q.get('cevap', '')[:200]}...
""")
        return "\n".join(formatted)
    
    def _parse_generated_questions(self, response_text: str) -> List[Dict]:
        """Gemini yanıtından soruları parse eder."""
        try:
            # JSON bloğunu bul
            json_match = re.search(r'\[[\s\S]*\]', response_text)
            if json_match:
                json_text = json_match.group()
                questions = json.loads(json_text)
                return questions
        except json.JSONDecodeError as e:
            print(f"JSON parse hatası: {e}")
        
        return []
    
    def predict_2026_trends(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        2026 LGS için konu ve soru trendlerini tahmin eder.
        
        Args:
            context: Analiz bağlamı
            
        Returns:
            Dict: Trend tahminleri
        """
        prompt = f"""Sen bir LGS eğitim uzmanısın. Geçmiş yılların LGS Türkçe soru analizine dayanarak 2026 LGS için tahminlerde bulun.

## VERİ ANALİZİ

### Kategori Dağılımı:
{json.dumps(context.get('category_trends', {}), ensure_ascii=False, indent=2)}

### Soru Kalıpları:
{json.dumps(context.get('question_patterns', {}), ensure_ascii=False, indent=2)}

### En Popüler Konular:
{', '.join([f"{kw[0]} ({kw[1]})" for kw in context.get('popular_topics', [])[:15]])}

## GÖREV

2026 LGS Türkçe sınavı için tahminlerini JSON formatında ver:

```json
{{
  "oncelikli_konular": ["En çok çıkması beklenen 5 konu"],
  "soru_dagilimi_tahmini": {{
    "Paragrafta Anlam": "Tahmini soru sayısı",
    "Cümlede Anlam": "Tahmini soru sayısı",
    "Sözcükte Anlam": "Tahmini soru sayısı",
    "Diğer": "Tahmini soru sayısı"
  }},
  "dikkat_edilmesi_gerekenler": ["Önemli noktalar listesi"],
  "yeni_trend_tahminleri": ["2026'da yeni çıkabilecek soru tipleri"],
  "onerilen_calisma_stratejisi": "Detaylı çalışma önerisi"
}}
```

Sadece JSON formatında yanıt ver.
"""
        
        try:
            response = self.model.generate_content(prompt)
            json_match = re.search(r'\{[\s\S]*\}', response.text)
            if json_match:
                return json.loads(json_match.group())
        except Exception as e:
            print(f"Trend tahmin hatası: {e}")
        
        return {}
    
    def analyze_question(self, question_text: str) -> Dict[str, Any]:
        """
        Verilen bir soruyu analiz eder.
        
        Args:
            question_text: Analiz edilecek soru metni
            
        Returns:
            Dict: Analiz sonuçları
        """
        prompt = f"""Aşağıdaki LGS Türkçe sorusunu analiz et:

SORU:
{question_text}

Aşağıdaki formatta JSON yanıt ver:

```json
{{
  "kategori": "Ana kategori (Paragrafta Anlam, Cümlede Anlam vb.)",
  "alt_kategori": "Alt kategori",
  "zorluk": "kolay/orta/zor",
  "kazanimlar": ["Bu sorunun ölçtüğü kazanımlar"],
  "ipuclari": ["Soruyu çözmek için ipuçları"],
  "benzer_soru_ozellikleri": "Bu tip sorularda dikkat edilecekler"
}}
```

Sadece JSON formatında yanıt ver.
"""
        
        try:
            response = self.model.generate_content(prompt)
            json_match = re.search(r'\{[\s\S]*\}', response.text)
            if json_match:
                return json.loads(json_match.group())
        except Exception as e:
            print(f"Soru analiz hatası: {e}")
        
        return {}
    
    def is_turkish_related(self, text: str) -> bool:
        """
        Metnin Türkçe dersiyle ilgili olup olmadığını kontrol eder.
        
        Args:
            text: Kontrol edilecek metin
            
        Returns:
            bool: Türkçe ile ilgiliyse True
        """
        # Diğer derslerle ilgili anahtar kelimeler
        other_subjects = [
            'matematik', 'denklem', 'geometri', 'sayı', 'işlem',
            'fen', 'fizik', 'kimya', 'biyoloji', 'deney',
            'sosyal', 'tarih', 'coğrafya', 'harita',
            'ingilizce', 'english', 'vocabulary',
            'din kültürü', 'ahlak'
        ]
        
        text_lower = text.lower()
        for subject in other_subjects:
            if subject in text_lower:
                return False
        
        # Türkçe ile ilgili anahtar kelimeler
        turkish_keywords = [
            'paragraf', 'cümle', 'sözcük', 'anlam', 'dil bilgisi',
            'yazım', 'noktalama', 'eş anlam', 'zıt anlam', 'mecaz',
            'deyim', 'atasözü', 'fiil', 'isim', 'sıfat', 'zarf',
            'anlatım', 'metin', 'okuma', 'yazar', 'şiir'
        ]
        
        for keyword in turkish_keywords:
            if keyword in text_lower:
                return True
        
        return True  # Varsayılan olarak Türkçe ile ilgili kabul et

