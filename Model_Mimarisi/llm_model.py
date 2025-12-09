"""
LGS Türkçe Soru Tahminleme Modeli - LLM Model Sınıfı
Gemini API kullanarak soru üretme ve tahminleme
"""

import google.generativeai as genai
from typing import List, Dict, Optional
import json
import re
from datetime import datetime

from config import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
    SYSTEM_PROMPT,
    QUESTION_GENERATION_PROMPT,
    TOPIC_DETECTION_PROMPT,
    TURKCE_KONULARI,
    ALT_KONULAR,
    ZORLUK_SEVIYELERI,
    KONU_DISI_UYARI
)
from data_processor import DataProcessor


class LGSTurkceModel:
    """LGS Türkçe soru tahminleme ve üretme modeli."""
    
    def __init__(self):
        """Modeli başlatır."""
        self._setup_gemini()
        self.data_processor = DataProcessor()
        self.generation_history = []
    
    def _setup_gemini(self):
        """Gemini API'yi yapılandırır."""
        if GEMINI_API_KEY == "BURAYA_API_ANAHTARINIZI_GIRIN":
            raise ValueError(
                "⚠️ Lütfen config.py dosyasında GEMINI_API_KEY değerini ayarlayın!\n"
                "API anahtarı almak için: https://makersuite.google.com/app/apikey"
            )
        
        genai.configure(api_key=GEMINI_API_KEY)
        
        # Model yapılandırması
        generation_config = {
            "temperature": 0.8,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 4096,
        }
        
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]
        
        self.model = genai.GenerativeModel(
            model_name=GEMINI_MODEL,
            generation_config=generation_config,
            safety_settings=safety_settings,
            system_instruction=SYSTEM_PROMPT
        )
        
        print(f"✅ LLM modeli yüklendi: {GEMINI_MODEL}")
    
    def is_turkce_related(self, text: str) -> bool:
        """Metnin Türkçe dersiyle ilgili olup olmadığını kontrol eder."""
        turkce_keywords = [
            "türkçe", "sözcük", "cümle", "paragraf", "anlam", "dil bilgisi",
            "yazım", "noktalama", "söz sanatı", "anlatım", "fiil", "isim",
            "sıfat", "zarf", "zamir", "edat", "bağlaç", "ünlem", "kip",
            "çatı", "tamlama", "özne", "yüklem", "nesne", "tümleç",
            "eş anlam", "zıt anlam", "mecaz", "benzetme", "kişileştirme",
            "virgül", "nokta", "soru", "üret", "oluştur", "hazırla",
            "lgs", "sınav", "test", "kolay", "orta", "zor", "deyim", "atasözü"
        ]
        
        diger_dersler = [
            "matematik", "toplama", "çıkarma", "çarpma", "bölme", "denklem",
            "geometri", "üçgen", "kare", "daire", "alan", "çevre", "hacim",
            "fen", "fizik", "kimya", "biyoloji", "hücre", "atom", "molekül",
            "enerji", "kuvvet", "hareket", "ısı", "elektrik", "mıknatıs",
            "sosyal", "tarih", "coğrafya", "vatandaşlık", "inkılap",
            "ingilizce", "english", "grammar", "vocabulary",
            "din", "ibadet", "namaz", "oruç", "zekat", "hac"
        ]
        
        text_lower = text.lower()
        
        # Diğer derslerle ilgili mi kontrol et
        for keyword in diger_dersler:
            if keyword in text_lower:
                return False
        
        return True
    
    def generate_questions(self, konu: str, zorluk: str = "Orta", 
                          adet: int = 3, alt_konu: str = None) -> str:
        """
        Belirli bir konuda soru üretir.
        
        Args:
            konu: Ana konu (örn: "Sözcükte Anlam")
            zorluk: Zorluk seviyesi ("Kolay", "Orta", "Zor")
            adet: Üretilecek soru sayısı
            alt_konu: Alt konu (isteğe bağlı)
        
        Returns:
            Üretilen sorular (metin olarak)
        """
        # Konu kontrolü
        if konu not in TURKCE_KONULARI:
            return f"❌ Geçersiz konu. Geçerli konular:\n{', '.join(TURKCE_KONULARI)}"
        
        # Zorluk kontrolü
        if zorluk not in ZORLUK_SEVIYELERI:
            zorluk = "Orta"
        
        # Örnek soruları getir
        examples = self.data_processor.get_examples_by_topic(konu, limit=5)
        
        if not examples:
            examples = self.data_processor.questions[:3]
        
        formatted_examples = self.data_processor.format_examples_for_prompt(examples)
        
        # Prompt oluştur
        prompt = QUESTION_GENERATION_PROMPT.format(
            konu=f"{konu}" + (f" - {alt_konu}" if alt_konu else ""),
            zorluk=zorluk,
            adet=adet,
            ornekler=formatted_examples
        )
        
        try:
            response = self.model.generate_content(prompt)
            generated_text = response.text
            
            # Üretim geçmişine ekle
            self.generation_history.append({
                "timestamp": datetime.now().isoformat(),
                "konu": konu,
                "alt_konu": alt_konu,
                "zorluk": zorluk,
                "adet": adet,
                "output": generated_text[:500]  # İlk 500 karakter
            })
            
            return generated_text
        
        except Exception as e:
            return f"❌ Soru üretilirken hata oluştu: {str(e)}"
    
    def predict_topic(self, soru_metni: str) -> str:
        """
        Bir sorunun hangi konuya ait olduğunu tahmin eder.
        
        Args:
            soru_metni: Analiz edilecek soru
        
        Returns:
            Tahmin edilen konu
        """
        if not self.is_turkce_related(soru_metni):
            return "Bu soru Türkçe dersiyle ilgili görünmüyor."
        
        prompt = TOPIC_DETECTION_PROMPT.format(
            soru=soru_metni,
            konular="\n".join([f"- {k}" for k in TURKCE_KONULARI])
        )
        
        try:
            response = self.model.generate_content(prompt)
            predicted_topic = response.text.strip()
            
            # Geçerli bir konu mu kontrol et
            for konu in TURKCE_KONULARI:
                if konu.lower() in predicted_topic.lower():
                    return konu
            
            return predicted_topic
        
        except Exception as e:
            return f"❌ Konu tahmininde hata: {str(e)}"
    
    def analyze_question(self, soru_metni: str) -> Dict:
        """
        Bir soruyu detaylı analiz eder.
        
        Args:
            soru_metni: Analiz edilecek soru
        
        Returns:
            Analiz sonuçları
        """
        if not self.is_turkce_related(soru_metni):
            return {"error": KONU_DISI_UYARI}
        
        prompt = f"""
{SYSTEM_PROMPT}

Aşağıdaki LGS Türkçe sorusunu analiz et:

SORU:
{soru_metni}

ANALİZ İÇERİĞİ:
1. Konu: (Ana konu nedir?)
2. Alt Konu: (Varsa alt konu nedir?)
3. Zorluk Tahmini: (Kolay/Orta/Zor)
4. Soru Tipi: (Bilgi/Anlama/Uygulama/Analiz)
5. Çözüm Stratejisi: (Bu soru nasıl çözülür?)
6. Dikkat Edilecek Noktalar: (Öğrencilerin dikkat etmesi gerekenler)

Her maddeyi detaylı açıkla.
"""
        
        try:
            response = self.model.generate_content(prompt)
            
            return {
                "soru": soru_metni,
                "analiz": response.text,
                "timestamp": datetime.now().isoformat()
            }
        
        except Exception as e:
            return {"error": f"Analiz hatası: {str(e)}"}
    
    def explain_topic(self, konu: str) -> str:
        """
        Bir konuyu detaylı açıklar.
        
        Args:
            konu: Açıklanacak konu
        
        Returns:
            Konu açıklaması
        """
        if not self.is_turkce_related(konu):
            return KONU_DISI_UYARI
        
        prompt = f"""
{SYSTEM_PROMPT}

"{konu}" konusunu LGS'ye hazırlanan 8. sınıf öğrencilerine uygun şekilde açıkla.

AÇIKLAMA İÇERİĞİ:
1. **Tanım**: Konunun ne olduğu
2. **Temel Kurallar**: Bilmesi gereken kurallar
3. **Örnekler**: Anlaşılır örnekler
4. **LGS'de Çıkış Şekli**: Sınavda nasıl sorulur
5. **İpuçları**: Soru çözerken dikkat edilecekler
6. **Sık Yapılan Hatalar**: Kaçınılması gereken hatalar

Açık, anlaşılır ve öğretici bir dil kullan. Örnekleri bol tut.
"""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        
        except Exception as e:
            return f"❌ Açıklama üretilirken hata: {str(e)}"
    
    def chat(self, user_message: str) -> str:
        """
        Kullanıcı ile sohbet eder.
        
        Args:
            user_message: Kullanıcı mesajı
        
        Returns:
            Model yanıtı
        """
        if not self.is_turkce_related(user_message):
            return KONU_DISI_UYARI
        
        prompt = f"""
{SYSTEM_PROMPT}

Kullanıcı sorusu: {user_message}

Türkçe dersiyle ilgili yardımcı bir yanıt ver. Eğer soru üretilmesi isteniyorsa,
LGS formatında (4 seçenekli) sorular üret ve cevaplarını açıkla.
"""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        
        except Exception as e:
            return f"❌ Yanıt üretilirken hata: {str(e)}"
    
    def get_model_stats(self) -> Dict:
        """Model istatistiklerini döndürür."""
        data_stats = self.data_processor.get_statistics()
        
        return {
            "model": GEMINI_MODEL,
            "toplam_soru": data_stats['toplam_soru'],
            "konulara_gore": data_stats['konulara_gore'],
            "zorluklara_gore": data_stats['zorluklara_gore'],
            "uretim_sayisi": len(self.generation_history)
        }


def main():
    """Test fonksiyonu."""
    print("🚀 LGS Türkçe Soru Tahminleme Modeli Test Ediliyor...")
    print("-" * 50)
    
    try:
        model = LGSTurkceModel()
        
        # Test 1: Soru üretme
        print("\n📝 Test 1: Soru Üretme")
        print("-" * 30)
        result = model.generate_questions(
            konu="Sözcükte Anlam",
            zorluk="Orta",
            adet=2
        )
        print(result[:800] + "..." if len(result) > 800 else result)
        
        # Test 2: Konu tahmini
        print("\n\n📊 Test 2: Konu Tahmini")
        print("-" * 30)
        test_soru = "Aşağıdaki cümlelerin hangisinde zıt anlamlı sözcükler bir arada kullanılmıştır?"
        konu = model.predict_topic(test_soru)
        print(f"Soru: {test_soru}")
        print(f"Tahmin Edilen Konu: {konu}")
        
        # Test 3: Konu dışı kontrol
        print("\n\n🚫 Test 3: Konu Dışı Kontrol")
        print("-" * 30)
        result = model.chat("Matematik denklem çöz")
        print(result)
        
        print("\n✅ Testler tamamlandı!")
        
    except ValueError as e:
        print(f"⚠️ {e}")


if __name__ == "__main__":
    main()

