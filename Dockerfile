FROM python:3.11-slim

# התקנת tesseract והרחבות לשפות עברית ואנגלית
RUN apt-get update && \
    apt-get install -y tesseract-ocr tesseract-ocr-heb tesseract-ocr-eng && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# יצירת תיקיית עבודה
WORKDIR /app

# העתקת הקבצים
COPY . .

# התקנת הדרישות
RUN pip install --no-cache-dir -r requirements.txt

# הרצת האפליקציה
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
