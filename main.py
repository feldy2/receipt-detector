from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
import pytesseract
import io

app = FastAPI()

KEYWORDS = ["קבלה", "מספר עסקה", "סה\"כ", "מע\"מ", "מסמך", "תאריך", "סכום", "לקוח", "תשלום"]

@app.post("/classify")
async def classify(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")
    
    # הפעלת OCR
    text = pytesseract.image_to_string(image, lang='heb+eng')
    
    # בדיקה אם הטקסט מכיל מילים שקשורות לקבלות
    if any(keyword in text for keyword in KEYWORDS):
        result = "קבלה"
    else:
        result = "לא קבלה"

    return JSONResponse(content={"label": result})
