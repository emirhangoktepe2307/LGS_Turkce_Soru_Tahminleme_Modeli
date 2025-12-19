"""
Hızlı Test Script - Soru Üretimi Testi
"""
import os
import sys

# Path ayarı
sys.path.insert(0, '.')

from dotenv import load_dotenv
load_dotenv('.env')
load_dotenv('../.env')

# API Key kontrolü
api_key = os.getenv('Gemini_API_Key', '')
if not api_key or len(api_key) < 10:
    print("❌ HATA: Gemini API Key bulunamadı!")
    print("   Lütfen .env dosyasında Gemini_API_Key değerini kontrol edin.")
    sys.exit(1)

print("✅ API Key mevcut")

# Data Analyzer testi
from model.data_analyzer import DataAnalyzer

print("\n📊 Veri Analizi Testi:")
print("-" * 40)

analyzer = DataAnalyzer('data.json')
print(f"   Toplam soru: {analyzer.get_total_questions()}")
print(f"   Kategoriler: {len(analyzer.get_category_distribution())}")

cat_dist = analyzer.get_category_distribution()
print("\n   Kategori Dağılımı:")
for cat, count in sorted(cat_dist.items(), key=lambda x: -x[1]):
    print(f"      {cat}: {count}")

# Soru üretimi testi
print("\n🤖 Soru Üretimi Testi:")
print("-" * 40)

from model.question_predictor import QuestionPredictor

predictor = QuestionPredictor(
    data_path='data.json',
    api_key=api_key
)

print("   Predictor hazır!")
print("   2 adet 'Paragrafta Anlam' sorusu üretiliyor...")

result = predictor.predict_questions(
    category="Paragrafta Anlam",
    count=2,
    difficulty="orta"
)

if result.get('success'):
    questions = result.get('generated_questions', [])
    print(f"\n   ✅ {len(questions)} soru üretildi!\n")
    
    for q in questions:
        print(f"   --- Soru {q.get('soru_no', '?')} ---")
        print(f"   Kategori: {q.get('kategori', 'Bilinmiyor')}")
        print(f"   Zorluk: {q.get('zorluk', 'Bilinmiyor')}")
        print(f"   Soru: {q.get('soru', '')[:100]}...")
        print(f"   Doğru Cevap: {q.get('dogru_cevap', '?')}")
        print()
else:
    print(f"   ❌ Hata: {result.get('error', 'Bilinmeyen hata')}")

print("\n✅ Test tamamlandı!")

