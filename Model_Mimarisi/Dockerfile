# LGS Türkçe Soru Üretici - Docker Dosyası
FROM python:3.10-slim

# Çalışma dizinini ayarla
WORKDIR /app

# Sistem bağımlılıklarını yükle
RUN apt-get update && apt-get install -y \
    build-essential \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Python bağımlılıklarını kopyala ve yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama dosyalarını kopyala
COPY . .

# ChromaDB veri dizinini oluştur
RUN mkdir -p /app/chroma_db

# Streamlit portu
EXPOSE 8501

# Sağlık kontrolü
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Uygulamayı başlat
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

