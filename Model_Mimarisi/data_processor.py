"""
LGS Türkçe Soru Tahminleme Modeli - Veri İşleme Modülü
Eğitim verilerini hazırlama ve işleme fonksiyonları
"""

import json
import random
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from datetime import datetime

from config import (
    QUESTIONS_DATA_FILE,
    TRAINING_DATA_FILE,
    GENERATED_QUESTIONS_FILE,
    TRAINING_CONFIG,
    TURKCE_KONULARI,
    DATA_DIR
)


class DataProcessor:
    """Veri işleme ve hazırlama sınıfı."""
    
    def __init__(self):
        """DataProcessor'ı başlatır."""
        self.questions = []
        self.training_data = []
        self._load_questions()
    
    def _load_questions(self):
        """Soru verilerini yükler."""
        if Path(QUESTIONS_DATA_FILE).exists():
            with open(QUESTIONS_DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.questions = data.get('sorular', [])
            print(f"✅ {len(self.questions)} soru yüklendi.")
        else:
            print(f"⚠️ Soru dosyası bulunamadı: {QUESTIONS_DATA_FILE}")
    
    def prepare_training_data(self) -> List[Dict]:
        """
        Soruları LLM eğitimi için hazırlar.
        Her soru için input-output çiftleri oluşturur.
        """
        training_examples = []
        
        for soru in self.questions:
            # Soru üretme eğitimi için örnek
            generation_example = {
                "type": "generation",
                "input": f"Konu: {soru['konu']}\nAlt Konu: {soru['alt_konu']}\nZorluk: {soru['zorluk']}\n\nBu konuda bir LGS sorusu üret.",
                "output": f"Soru:\n{soru['soru_metni']}\n\nDoğru Cevap: {soru['dogru_cevap']}\n\nAçıklama: {soru['cevap_aciklamasi']}",
                "metadata": {
                    "konu": soru['konu'],
                    "alt_konu": soru['alt_konu'],
                    "zorluk": soru['zorluk']
                }
            }
            training_examples.append(generation_example)
            
            # Konu tespiti eğitimi için örnek
            classification_example = {
                "type": "classification",
                "input": f"Bu sorunun konusunu belirle:\n{soru['soru_metni']}",
                "output": soru['konu'],
                "metadata": {
                    "konu": soru['konu'],
                    "alt_konu": soru['alt_konu']
                }
            }
            training_examples.append(classification_example)
        
        self.training_data = training_examples
        return training_examples
    
    def split_data(self) -> Tuple[List[Dict], List[Dict], List[Dict]]:
        """
        Veriyi eğitim, doğrulama ve test setlerine böler.
        """
        if not self.training_data:
            self.prepare_training_data()
        
        # Veriyi karıştır
        data = self.training_data.copy()
        random.shuffle(data)
        
        # Bölme oranları
        train_ratio = TRAINING_CONFIG['train_split']
        val_ratio = TRAINING_CONFIG['validation_split']
        
        # İndeksler
        total = len(data)
        train_end = int(total * train_ratio)
        val_end = train_end + int(total * val_ratio)
        
        train_data = data[:train_end]
        val_data = data[train_end:val_end]
        test_data = data[val_end:]
        
        print(f"📊 Veri bölündü:")
        print(f"   Eğitim: {len(train_data)}")
        print(f"   Doğrulama: {len(val_data)}")
        print(f"   Test: {len(test_data)}")
        
        return train_data, val_data, test_data
    
    def get_examples_by_topic(self, konu: str, limit: int = 5) -> List[Dict]:
        """Belirli bir konudan örnek sorular getirir."""
        examples = [q for q in self.questions if q['konu'] == konu]
        
        if len(examples) > limit:
            examples = random.sample(examples, limit)
        
        return examples
    
    def get_examples_by_difficulty(self, zorluk: str, limit: int = 5) -> List[Dict]:
        """Belirli bir zorluktan örnek sorular getirir."""
        examples = [q for q in self.questions if q['zorluk'] == zorluk]
        
        if len(examples) > limit:
            examples = random.sample(examples, limit)
        
        return examples
    
    def format_examples_for_prompt(self, examples: List[Dict]) -> str:
        """Örnekleri prompt için formatlar."""
        formatted = []
        
        for i, ex in enumerate(examples, 1):
            formatted.append(f"""
--- Örnek {i} ---
Konu: {ex['konu']} - {ex['alt_konu']}
Zorluk: {ex['zorluk']}

{ex['soru_metni']}

Doğru Cevap: {ex['dogru_cevap']}
Açıklama: {ex['cevap_aciklamasi']}
""")
        
        return "\n".join(formatted)
    
    def save_training_data(self):
        """Eğitim verilerini dosyaya kaydeder."""
        if not self.training_data:
            self.prepare_training_data()
        
        output = {
            "created_at": datetime.now().isoformat(),
            "total_examples": len(self.training_data),
            "examples": self.training_data
        }
        
        with open(TRAINING_DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Eğitim verisi kaydedildi: {TRAINING_DATA_FILE}")
    
    def get_statistics(self) -> Dict:
        """Veri istatistiklerini döndürür."""
        stats = {
            "toplam_soru": len(self.questions),
            "konulara_gore": {},
            "zorluklara_gore": {},
            "yillara_gore": {}
        }
        
        for soru in self.questions:
            # Konuya göre
            konu = soru.get('konu', 'Bilinmiyor')
            stats['konulara_gore'][konu] = stats['konulara_gore'].get(konu, 0) + 1
            
            # Zorluğa göre
            zorluk = soru.get('zorluk', 'Bilinmiyor')
            stats['zorluklara_gore'][zorluk] = stats['zorluklara_gore'].get(zorluk, 0) + 1
            
            # Yıla göre
            yil = soru.get('yil', 'Bilinmiyor')
            stats['yillara_gore'][yil] = stats['yillara_gore'].get(yil, 0) + 1
        
        return stats
    
    def add_generated_question(self, soru: Dict):
        """Üretilen soruyu kaydeder."""
        generated_file = Path(GENERATED_QUESTIONS_FILE)
        
        if generated_file.exists():
            with open(generated_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = {"sorular": []}
        
        soru['generated_at'] = datetime.now().isoformat()
        data['sorular'].append(soru)
        
        with open(generated_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def validate_question_format(self, soru_text: str) -> bool:
        """Soru formatının geçerliliğini kontrol eder."""
        # A), B), C), D) seçenekleri var mı kontrol et
        required_options = ['A)', 'B)', 'C)', 'D)']
        
        for option in required_options:
            if option not in soru_text and option.replace(')', '.') not in soru_text:
                return False
        
        return True


def main():
    """Test fonksiyonu."""
    print("🔧 Veri İşleme Modülü Test Ediliyor...")
    print("-" * 50)
    
    processor = DataProcessor()
    
    # İstatistikleri göster
    stats = processor.get_statistics()
    print(f"\n📊 Veri İstatistikleri:")
    print(f"   Toplam Soru: {stats['toplam_soru']}")
    print(f"   Konulara Göre: {stats['konulara_gore']}")
    print(f"   Zorluklara Göre: {stats['zorluklara_gore']}")
    
    # Eğitim verisi hazırla
    print("\n📝 Eğitim verisi hazırlanıyor...")
    training_data = processor.prepare_training_data()
    print(f"   Toplam örnek: {len(training_data)}")
    
    # Veriyi böl
    train, val, test = processor.split_data()
    
    # Kaydet
    processor.save_training_data()
    
    print("\n✅ Test tamamlandı!")


if __name__ == "__main__":
    main()

