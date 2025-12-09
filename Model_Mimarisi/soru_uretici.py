"""
LGS Türkçe Soru Üretici Modülü
Bu dosya, üretilen soruları veritabanına kaydeder ve yönetir.
"""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import re
from config import DATA_FILE, TURKCE_KONULARI, ALT_KONULAR, ZORLUK_SEVIYELERI


class SoruYoneticisi:
    """Soru üretme ve veritabanı yönetimi sınıfı."""
    
    def __init__(self, data_file: str = DATA_FILE):
        """Soru yöneticisini başlatır."""
        self.data_file = data_file
        self.data = self._load_data()
    
    def _load_data(self) -> dict:
        """Mevcut verileri yükler."""
        if Path(self.data_file).exists():
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "metadata": {
                "ders": "Türkçe",
                "sinav": "LGS",
                "yillar": [],
                "konu_basliklari": TURKCE_KONULARI
            },
            "sorular": []
        }
    
    def _save_data(self):
        """Verileri dosyaya kaydeder."""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)
    
    def generate_id(self) -> str:
        """Benzersiz soru ID'si oluşturur."""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        return f"LGS-TR-GEN-{timestamp}-{unique_id}"
    
    def parse_generated_question(self, generated_text: str) -> List[Dict]:
        """Gemini'nin ürettiği metinden soruları ayrıştırır."""
        sorular = []
        
        # Soru bloklarını bul (numaralı veya "Soru" ile başlayan)
        soru_patterns = [
            r'(?:Soru\s*\d*[:.]?\s*|^\d+[.)]\s*)(.*?)(?=(?:Soru\s*\d*[:.]?|^\d+[.)]|\Z))',
            r'(?:\*\*Soru\s*\d*\*\*[:.]?\s*)(.*?)(?=(?:\*\*Soru|\Z))'
        ]
        
        # Basit ayrıştırma - her "Soru" veya numara ile başlayan bloğu yakala
        blocks = re.split(r'\n(?=\d+[.)]\s*|\*\*Soru|Soru\s*\d+)', generated_text)
        
        for block in blocks:
            if not block.strip():
                continue
            
            soru_dict = self._extract_question_parts(block)
            if soru_dict and soru_dict.get('soru_metni'):
                sorular.append(soru_dict)
        
        return sorular
    
    def _extract_question_parts(self, block: str) -> Optional[Dict]:
        """Bir soru bloğundan parçaları çıkarır."""
        try:
            # Seçenekleri bul
            secenekler = re.findall(r'[A-D][.)]\s*(.+?)(?=\n[A-D][.)]|\n\n|$)', block, re.DOTALL)
            
            if len(secenekler) < 4:
                return None
            
            # Soru metnini bul (seçeneklerden önce)
            soru_match = re.search(r'^.*?(?=\nA[.)])', block, re.DOTALL)
            if not soru_match:
                return None
            
            soru_metni = soru_match.group().strip()
            # Numara ve "Soru" kelimesini temizle
            soru_metni = re.sub(r'^[\d.)\s]*(?:Soru\s*\d*[:.]?\s*|\*\*Soru\s*\d*\*\*[:.]?\s*)?', '', soru_metni).strip()
            
            # Doğru cevabı bul
            dogru_cevap = ""
            cevap_patterns = [
                r'(?:Doğru\s*[Cc]evap|Cevap)[:.\s]*([A-D])',
                r'\*\*([A-D])\*\*',
                r'([A-D])\s*(?:doğrudur|seçeneği)'
            ]
            
            for pattern in cevap_patterns:
                match = re.search(pattern, block, re.IGNORECASE)
                if match:
                    dogru_cevap = match.group(1).upper()
                    break
            
            # Açıklamayı bul
            aciklama_patterns = [
                r'(?:Açıklama|Çözüm)[:.\s]*(.+?)(?=\n\n|\Z)',
                r'(?:Neden|Çünkü)[:.\s]*(.+?)(?=\n\n|\Z)'
            ]
            
            aciklama = ""
            for pattern in aciklama_patterns:
                match = re.search(pattern, block, re.IGNORECASE | re.DOTALL)
                if match:
                    aciklama = match.group(1).strip()
                    break
            
            # Soru metnini seçeneklerle birleştir
            formatted_soru = soru_metni + "\n\n"
            for i, secenek in enumerate(secenekler[:4]):
                formatted_soru += f"{chr(65+i)}) {secenek.strip()}\n"
            
            return {
                "soru_metni": formatted_soru.strip(),
                "dogru_cevap": dogru_cevap or "A",
                "cevap_aciklamasi": aciklama or "Açıklama mevcut değil.",
                "secenekler": {
                    "A": secenekler[0].strip() if len(secenekler) > 0 else "",
                    "B": secenekler[1].strip() if len(secenekler) > 1 else "",
                    "C": secenekler[2].strip() if len(secenekler) > 2 else "",
                    "D": secenekler[3].strip() if len(secenekler) > 3 else ""
                }
            }
        except Exception as e:
            print(f"⚠️ Soru ayrıştırma hatası: {e}")
            return None
    
    def add_question(self, soru_metni: str, dogru_cevap: str, 
                    cevap_aciklamasi: str, konu: str, alt_konu: str = "",
                    zorluk: str = "Orta", anahtar_kelimeler: List[str] = None) -> str:
        """Yeni soru ekler ve ID'sini döndürür."""
        
        # Validasyon
        if konu not in TURKCE_KONULARI:
            raise ValueError(f"Geçersiz konu: {konu}")
        
        if zorluk not in ZORLUK_SEVIYELERI:
            zorluk = "Orta"
        
        if dogru_cevap not in ["A", "B", "C", "D"]:
            dogru_cevap = "A"
        
        # Yeni soru oluştur
        soru_id = self.generate_id()
        yeni_soru = {
            "id": soru_id,
            "yil": "AI-Üretimi",
            "konu": konu,
            "alt_konu": alt_konu or "Genel",
            "soru_metni": soru_metni,
            "dogru_cevap": dogru_cevap,
            "cevap_aciklamasi": cevap_aciklamasi,
            "zorluk": zorluk,
            "anahtar_kelimeler": anahtar_kelimeler or [],
            "olusturma_tarihi": datetime.now().isoformat(),
            "kaynak": "Gemini AI"
        }
        
        self.data["sorular"].append(yeni_soru)
        self._save_data()
        
        return soru_id
    
    def add_questions_batch(self, sorular: List[Dict], konu: str, 
                           alt_konu: str = "", zorluk: str = "Orta") -> List[str]:
        """Toplu soru ekler."""
        added_ids = []
        
        for soru in sorular:
            try:
                soru_id = self.add_question(
                    soru_metni=soru.get("soru_metni", ""),
                    dogru_cevap=soru.get("dogru_cevap", "A"),
                    cevap_aciklamasi=soru.get("cevap_aciklamasi", ""),
                    konu=konu,
                    alt_konu=alt_konu,
                    zorluk=zorluk,
                    anahtar_kelimeler=soru.get("anahtar_kelimeler", [])
                )
                added_ids.append(soru_id)
            except Exception as e:
                print(f"⚠️ Soru eklenirken hata: {e}")
        
        return added_ids
    
    def get_questions_by_topic(self, konu: str, alt_konu: str = None, 
                               limit: int = 10) -> List[Dict]:
        """Konuya göre soruları getirir."""
        filtered = []
        
        for soru in self.data["sorular"]:
            if soru["konu"] == konu:
                if alt_konu is None or soru["alt_konu"] == alt_konu:
                    filtered.append(soru)
                    if len(filtered) >= limit:
                        break
        
        return filtered
    
    def get_questions_by_difficulty(self, zorluk: str, limit: int = 10) -> List[Dict]:
        """Zorluğa göre soruları getirir."""
        filtered = []
        
        for soru in self.data["sorular"]:
            if soru["zorluk"] == zorluk:
                filtered.append(soru)
                if len(filtered) >= limit:
                    break
        
        return filtered
    
    def get_random_questions(self, adet: int = 10, konu: str = None) -> List[Dict]:
        """Rastgele soru seçer."""
        import random
        
        sorular = self.data["sorular"]
        
        if konu:
            sorular = [s for s in sorular if s["konu"] == konu]
        
        if len(sorular) <= adet:
            return sorular
        
        return random.sample(sorular, adet)
    
    def get_statistics(self) -> Dict:
        """Veritabanı istatistiklerini döndürür."""
        stats = {
            "toplam_soru": len(self.data["sorular"]),
            "konulara_gore": {},
            "zorluklara_gore": {},
            "ai_uretimi": 0,
            "gercek_sinav": 0
        }
        
        for soru in self.data["sorular"]:
            # Konuya göre
            konu = soru.get("konu", "Bilinmiyor")
            stats["konulara_gore"][konu] = stats["konulara_gore"].get(konu, 0) + 1
            
            # Zorluğa göre
            zorluk = soru.get("zorluk", "Bilinmiyor")
            stats["zorluklara_gore"][zorluk] = stats["zorluklara_gore"].get(zorluk, 0) + 1
            
            # Kaynağa göre
            if soru.get("yil") == "AI-Üretimi":
                stats["ai_uretimi"] += 1
            else:
                stats["gercek_sinav"] += 1
        
        return stats
    
    def delete_question(self, soru_id: str) -> bool:
        """Soru siler."""
        for i, soru in enumerate(self.data["sorular"]):
            if soru["id"] == soru_id:
                del self.data["sorular"][i]
                self._save_data()
                return True
        return False
    
    def export_to_json(self, output_file: str = None) -> str:
        """Soruları JSON dosyasına aktarır."""
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"lgs_turkce_export_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)
        
        return output_file


def main():
    """Test fonksiyonu."""
    print("🧪 Soru Yöneticisi Test Ediliyor...")
    print("-" * 50)
    
    yonetici = SoruYoneticisi()
    
    # İstatistikleri göster
    stats = yonetici.get_statistics()
    print(f"📊 Toplam Soru: {stats['toplam_soru']}")
    print(f"📚 Konulara Göre: {stats['konulara_gore']}")
    print(f"📈 Zorluklara Göre: {stats['zorluklara_gore']}")
    
    # Örnek soru ekleme
    print("\n➕ Örnek soru ekleniyor...")
    soru_id = yonetici.add_question(
        soru_metni="""Aşağıdaki cümlelerin hangisinde deyim kullanılmıştır?

A) Bugün hava çok güzel.
B) Ali işi sağlama aldı.
C) Kitabı rafa koydum.
D) Çocuklar bahçede oynuyor.""",
        dogru_cevap="B",
        cevap_aciklamasi="'Sağlama almak' bir deyimdir ve 'emin olmak, garantiye almak' anlamında kullanılır.",
        konu="Sözcükte Anlam",
        alt_konu="Deyimler",
        zorluk="Kolay",
        anahtar_kelimeler=["deyim", "sözcük anlamı", "kalıplaşmış söz"]
    )
    print(f"✅ Soru eklendi: {soru_id}")
    
    # Güncel istatistikler
    stats = yonetici.get_statistics()
    print(f"\n📊 Güncel Toplam Soru: {stats['toplam_soru']}")
    print(f"🤖 AI Üretimi: {stats['ai_uretimi']}")


if __name__ == "__main__":
    main()

