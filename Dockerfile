# תשתית עם פייתון
FROM python:3.11-slim

# התקנת Tesseract
RUN apt-get update && \
    apt-get install -y tesseract-ocr tesseract-ocr-heb tesseract-ocr-eng && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# העתקת הקוד
WORKDIR /app
COPY . /app

# התקנת תלויות
RUN pip install --no-cache-dir -r requirements.txt

# הרצת השרת
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
