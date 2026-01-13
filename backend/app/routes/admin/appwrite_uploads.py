from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from app.auth.deps import get_current_user
from appwrite.client import Client
from appwrite.services.storage import Storage
from appwrite.id import ID
from appwrite.input_file import InputFile
from app.config import (
    APPWRITE_API_KEY,
    APPWRITE_BUCKET_ID,
    APPWRITE_ENDPOINT,
    APPWRITE_PROJECT_ID
)

router = APIRouter(
    prefix="/admin/uploads",
    tags=["Uploads"],
)

def get_storage() -> Storage:
    client = Client()
    client.set_endpoint(APPWRITE_ENDPOINT)
    client.set_project(APPWRITE_PROJECT_ID)
    client.set_key(APPWRITE_API_KEY)
    return Storage(client)

@router.post("/image")
async def upload_image(
    file: UploadFile = File(...),
    admin = Depends(get_current_user)
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid image type")
    
    storage = get_storage()

    try:
        file_bytes = await file.read()
        input_file = InputFile.from_bytes(
            file_bytes,
            filename=file.filename,
            mime_type = file.content_type,
        )
        result = storage.create_file(
            bucket_id=APPWRITE_BUCKET_ID,
            file_id=ID.unique(),
            file=input_file,
        )
    except Exception as e:
        print("APPWRITE ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))
    
    return {
        "image_url":f"appwrite://{APPWRITE_BUCKET_ID}/{result['$id']}"
    }
