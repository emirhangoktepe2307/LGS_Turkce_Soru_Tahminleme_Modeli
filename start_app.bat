@echo off
echo LGS Soru Tahmin Uygulamasi Baslatiliyor...
echo.

if exist venv (
    echo Sanal ortam aktif ediliyor...
    call venv\Scripts\activate
) else (
    echo UYARI: 'venv' klasoru bulunamadi. Lutfen sanal ortami olusturun.
    pause
    exit
)

echo Bagimliliklar kontrol ediliyor...
pip install -r requirements.txt

echo.
echo Tarayici aciliyor...
start http://localhost:8000

echo.
echo Backend sunucusu baslatiliyor (Durdurmak icin CTRL+C)...
python main.py

pause
