@echo off
echo ========================================
echo   LGS Turkce Soru Tahminleme Modeli
echo   LLM Tabanli Yapay Zeka Sistemi
echo ========================================
echo.

REM Python kontrolu
python --version >nul 2>&1
if errorlevel 1 (
    echo [HATA] Python bulunamadi! Lutfen Python 3.9+ yukleyin.
    pause
    exit /b 1
)

echo [1/2] Gerekli kutuphaneler yukleniyor...
pip install -r requirements.txt -q

echo [2/2] Uygulama baslatiliyor...
echo.
echo Tarayicinizda http://localhost:8501 adresine gidin
echo Kapatmak icin Ctrl+C tuslarina basin
echo.
streamlit run app.py

pause
