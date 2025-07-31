from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import shutil
import os
from main import process_audio

app = FastAPI()
UPLOAD_DIRECTORY = "uploaded_files"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)
ALLOWED_FILE_TYPES = ["audio/wav", "audio/x-wav", "audio/mpeg"]
@app.post("/upload-audio")
async def upload_audio(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_FILE_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only .wav and .mp3 files are allowed."
        )
    
    file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)

    with open(file_path, "wb") as new_file:
        shutil.copyfileobj(file.file, new_file)
    
    return {
        "status": 200,
        "message": "File uploaded successfully",
        "path": file_path
    }

@app.post("/full-pipeline")
async def full_pipeline(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    df, timing_data, review_output = process_audio(file_path)

    response = {
        "status": 200,
        "speakers": df.to_dict(orient="records"),
        "timing_data": timing_data,
        "review_output": review_output,
    }

    return JSONResponse(content=response)