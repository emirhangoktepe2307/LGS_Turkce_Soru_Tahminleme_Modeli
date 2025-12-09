# LGS Türkçe Soru Tahminleme Modeli - PowerShell Başlatma Scripti

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  LGS Türkçe Soru Tahminleme Modeli" -ForegroundColor Yellow
Write-Host "  LLM Tabanlı Yapay Zeka Sistemi" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Python kontrolü
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[OK] Python bulundu: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[HATA] Python bulunamadı! Lütfen Python 3.9+ yükleyin." -ForegroundColor Red
    exit 1
}

# Kütüphaneleri yükle
Write-Host ""
Write-Host "[1/2] Gerekli kütüphaneler yükleniyor..." -ForegroundColor Cyan
pip install -r requirements.txt -q

# Uygulamayı başlat
Write-Host "[2/2] Uygulama başlatılıyor..." -ForegroundColor Cyan
Write-Host ""
Write-Host "Tarayıcınızda http://localhost:8501 adresine gidin" -ForegroundColor Green
Write-Host "Kapatmak için Ctrl+C tuşlarına basın" -ForegroundColor Yellow
Write-Host ""

streamlit run app.py
