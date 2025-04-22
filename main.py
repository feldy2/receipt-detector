from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
import pytesseract
import io
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import os

app = FastAPI()

KEYWORDS = ["קבלה", "מספר עסקה", "סה\"כ", "מע\"מ", "מסמך", "תאריך", "סכום", "לקוח", "תשלום"]

# === Google Drive Setup ===
SCOPES = ['https://www.googleapis.com/auth/drive.file']
SERVICE_ACCOUNT_FILE = 'path/to/your/service_account.json'  # עדכני כאן
DRIVE_FOLDER_ID = 'your_drive_folder_id_here'  # עדכני כאן

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
drive_service = build('drive', 'v3', credentials=credentials)

def upload_to_drive_bytes(file_bytes: bytes, filename: str, folder_id: str) -> str:
    file_metadata = {
        'name': filename,
        'parents': [folder_id]
    }
    media = MediaIoBaseUpload(io.BytesIO(file_bytes), mimetype='image/jpeg', resumable=True)
    file = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()
    return file.get('id')

# === Endpoint ===
@app.post("/classify")
async def classify(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")

    # OCR
    text = pytesseract.image_to_string(image, lang='heb+eng')

    # Classification
    if any(keyword in text for keyword in KEYWORDS):
        result = "קבלה"

        # Upload to Drive
        try:
            file_id = upload_to_drive_bytes(contents, file.filename, DRIVE_FOLDER_ID)
            return JSONResponse(content={"label": result, "uploaded": True, "file_id": file_id})
        except Exception as e:
            return JSONResponse(content={"label": result, "uploaded": False, "error": str(e)})
    else:
        return JSONResponse(content={"label": "לא קבלה", "uploaded": False})
