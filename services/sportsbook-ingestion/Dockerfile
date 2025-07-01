# Dockerfile inside sportsbook-ingestion
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Install playwright and browsers
RUN apt-get update && apt-get install -y \
    curl \
    libglib2.0-0 \
    libgdk-pixbuf-2.0-0 \
    libnspr4 \
    libnss3 \
    libdbus-1-3 \
    libatk1.0-0 \
    libexpat1 \
    libatspi2.0-0 \
    libx11-6 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libxcb1 \
    libxkbcommon0 \
    libasound2 \
    libgtk-3-0 \
    libxshmfence1 \
    ca-certificates \
    fonts-liberation \
    libappindicator3-1 \
    lsb-release \
    xdg-utils \
    wget && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN playwright install

COPY . .

CMD ["python", "app.py"]