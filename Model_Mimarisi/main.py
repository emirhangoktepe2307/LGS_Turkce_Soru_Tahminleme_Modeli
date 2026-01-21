"""
LGS Türkçe Soru Tahminleme Modeli - Ana Uygulama
Hibrit Model: Veri Analizi + Gemini API

Kullanım:
    API Sunucusu: python main.py --api
    CLI Modu: python main.py --cli
"""

import argparse
import sys
from pathlib import Path

# Proje kök dizinini path'e ekle
BASE_DIR = Path(__file__).parent
sys.path.insert(0, str(BASE_DIR))


def run_api_server(host: str = "0.0.0.0", port: int = 8000):
    """FastAPI sunucusunu başlatır."""
    import uvicorn
    from api.endpoints import app
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║         🎓 LGS Türkçe Soru Tahminleme API                    ║
╠══════════════════════════════════════════════════════════════╣
║  API Dokumentasyon: http://{host}:{port}/docs                    ║
║  ReDoc: http://{host}:{port}/redoc                               ║
║  API Base: http://{host}:{port}/api/v1                           ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    uvicorn.run(app, host=host, port=port, reload=False)


def run_cli_mode():
    """CLI modunda çalıştırır."""
    import os
    from dotenv import load_dotenv
    from model.question_predictor import QuestionPredictor
    
    # .env yükle
    load_dotenv(BASE_DIR / ".env")
    load_dotenv(BASE_DIR.parent / ".env")
    
    api_key = os.getenv("Gemini_API_Key", "")
    data_file = BASE_DIR / "data.json"
    
    if not api_key or api_key == "BURAYA_API_ANAHTARINIZI_GIRIN":
        print("❌ Hata: Gemini API anahtarı bulunamadı!")
        print("   .env dosyasında Gemini_API_Key değerini ayarlayın.")
        return
    
    if not data_file.exists():
        print(f"❌ Hata: Veri dosyası bulunamadı: {data_file}")
        return
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║         🎓 LGS Türkçe Soru Tahminleme CLI                    ║
╠══════════════════════════════════════════════════════════════╣
║  Komutlar:                                                   ║
║    1 - Soru üret                                             ║
║    2 - 2026 trend tahminleri                                 ║
║    3 - Kategori istatistikleri                               ║
║    4 - Örnek sorular                                         ║
║    5 - Soru analizi                                          ║
║    0 - Çıkış                                                 ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    predictor = QuestionPredictor(
        data_path=str(data_file),
        api_key=api_key
    )
    
    while True:
        try:
            choice = input("\n📌 Seçiminiz (0-5): ").strip()
            
            if choice == "0":
                print("👋 Güle güle!")
                break
            
            elif choice == "1":
                print("\n📚 Kategoriler:")
                for i, cat in enumerate(QuestionPredictor.SUPPORTED_CATEGORIES, 1):
                    print(f"   {i}. {cat}")
                
                cat_idx = int(input("Kategori numarası (0=rastgele): ")) - 1
                category = None
                if 0 <= cat_idx < len(QuestionPredictor.SUPPORTED_CATEGORIES):
                    category = QuestionPredictor.SUPPORTED_CATEGORIES[cat_idx]
                
                count = int(input("Soru sayısı (1-10): "))
                difficulty = input("Zorluk (kolay/orta/zor): ").strip().lower() or "orta"
                
                print("\n⏳ Sorular üretiliyor...")
                result = predictor.predict_questions(
                    category=category,
                    count=count,
                    difficulty=difficulty
                )
                
                if result.get("success"):
                    questions = result.get("generated_questions", [])
                    print(f"\n✅ {len(questions)} soru üretildi:\n")
                    for q in questions:
                        print(f"--- Soru {q.get('soru_no', '?')} ---")
                        print(f"Kategori: {q.get('kategori', 'Bilinmiyor')}")
                        if q.get('metin'):
                            print(f"Metin: {q.get('metin', '')[:200]}...")
                        print(f"Soru: {q.get('soru', '')}")
                        print("Şıklar:")
                        for k, v in q.get('secenekler', {}).items():
                            print(f"   {k}) {v}")
                        print(f"Doğru Cevap: {q.get('dogru_cevap', '?')}")
                        print(f"Açıklama: {q.get('aciklama', '')[:150]}...")
                        print()
                else:
                    print(f"❌ Hata: {result.get('error', 'Bilinmeyen hata')}")
            
            elif choice == "2":
                print("\n⏳ 2026 trend tahminleri hesaplanıyor...")
                predictions = predictor.get_2026_predictions()
                
                trends = predictions.get("trend_predictions", {})
                print("\n📈 2026 LGS Türkçe Tahminleri:")
                print("-" * 50)
                
                if trends.get("oncelikli_konular"):
                    print("\n🎯 Öncelikli Konular:")
                    for konu in trends["oncelikli_konular"]:
                        print(f"   • {konu}")
                
                if trends.get("dikkat_edilmesi_gerekenler"):
                    print("\n⚠️ Dikkat Edilmesi Gerekenler:")
                    for item in trends["dikkat_edilmesi_gerekenler"]:
                        print(f"   • {item}")
                
                if trends.get("onerilen_calisma_stratejisi"):
                    print(f"\n📖 Çalışma Stratejisi:")
                    print(f"   {trends['onerilen_calisma_stratejisi']}")
            
            elif choice == "3":
                stats = predictor.get_category_statistics()
                print("\n📊 Kategori İstatistikleri:")
                print("-" * 50)
                
                cat_dist = stats.get("category_distribution", {})
                total = sum(cat_dist.values())
                
                for cat, count in sorted(cat_dist.items(), key=lambda x: -x[1]):
                    pct = (count / total * 100) if total > 0 else 0
                    bar = "█" * int(pct / 5)
                    print(f"   {cat}: {count} ({pct:.1f}%) {bar}")
                
                print(f"\n   Toplam: {total} soru")
            
            elif choice == "4":
                print("\n📚 Kategoriler:")
                for i, cat in enumerate(QuestionPredictor.SUPPORTED_CATEGORIES, 1):
                    print(f"   {i}. {cat}")
                
                cat_idx = int(input("Kategori numarası: ")) - 1
                if 0 <= cat_idx < len(QuestionPredictor.SUPPORTED_CATEGORIES):
                    category = QuestionPredictor.SUPPORTED_CATEGORIES[cat_idx]
                    samples = predictor.get_sample_questions_by_category(category, 3)
                    
                    print(f"\n📝 {category} - Örnek Sorular:\n")
                    for i, q in enumerate(samples, 1):
                        print(f"--- Örnek {i} ---")
                        print(f"Alt Başlık: {q.get('alt_baslik', '')}")
                        print(f"Soru: {q.get('soru_koku', '')[:150]}...")
                        print()
            
            elif choice == "5":
                question = input("\nAnaliz edilecek soruyu girin:\n> ")
                print("\n⏳ Soru analiz ediliyor...")
                
                analysis = predictor.analyze_question(question)
                
                if "error" not in analysis:
                    result = analysis.get("analysis", {})
                    print("\n🔍 Analiz Sonucu:")
                    print(f"   Kategori: {result.get('kategori', 'Bilinmiyor')}")
                    print(f"   Alt Kategori: {result.get('alt_kategori', 'Bilinmiyor')}")
                    print(f"   Zorluk: {result.get('zorluk', 'Bilinmiyor')}")
                    
                    if result.get("ipuclari"):
                        print("\n   💡 İpuçları:")
                        for ipucu in result["ipuclari"]:
                            print(f"      • {ipucu}")
                else:
                    print(f"❌ {analysis.get('error')}")
            
            else:
                print("❓ Geçersiz seçim. 0-5 arasında bir numara girin.")
        
        except KeyboardInterrupt:
            print("\n👋 Güle güle!")
            break
        except Exception as e:
            print(f"❌ Hata: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="LGS Türkçe Soru Tahminleme Modeli"
    )
    parser.add_argument(
        "--api", 
        action="store_true",
        help="REST API sunucusunu başlat"
    )
    parser.add_argument(
        "--cli",
        action="store_true", 
        help="CLI modunda çalıştır"
    )
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="API sunucu host adresi (varsayılan: 0.0.0.0)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="API sunucu port numarası (varsayılan: 8000)"
    )
    
    args = parser.parse_args()
    
    if args.api:
        run_api_server(args.host, args.port)
    elif args.cli:
        run_cli_mode()
    else:
        # Varsayılan olarak API sunucusunu başlat
        print("Kullanım: python main.py --api veya python main.py --cli")
        print("--api: REST API sunucusunu başlatır")
        print("--cli: Komut satırı arayüzünü başlatır")


if __name__ == "__main__":
    main()

