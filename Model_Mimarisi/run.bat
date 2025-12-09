@echo off
echo ========================================
echo   LGS Turkce Soru Uretici
echo   Yapay Zeka Destekli Soru Sistemi
echo ========================================
echo.

REM Python kontrolu
python --version >nul 2>&1
if errorlevel 1 (
    echo [HATA] Python bulunamadi! Lutfen Python 3.9+ yukleyin.
    pause
    exit /b 1
)

echo [1/3] Gerekli kutuphaneler kontrol ediliyor...
pip install -r requirements.txt -q

echo [2/3] Veritabani baslatilidyor...
python turkce_chroma_setup.py

echo [3/3] Uygulama baslatiliyor...
echo.
echo Tarayicinizda http://localhost:8501 adresine gidin
echo Kapatmak icin Ctrl+C tuslarina basin
echo.
streamlit run app.py

pause

