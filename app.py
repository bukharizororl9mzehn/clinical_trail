from fastapi import FastAPI, UploadFile, File, HTTPException
from utils.redis_cache import get_cached_text, cache_text
from utils.pdf_utils import extract_text_from_pdf

app = FastAPI()

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    # Validate file extension and MIME type
    if not file.filename.lower().endswith(".pdf") or file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="File must be a valid PDF.")

    # Check Redis cache
    cached = get_cached_text(file.filename)
    if cached:
        return {
            "filename": file.filename,
            "status": "cached",
            "text": cached[:1000]  # Return preview only
        }

    # Ensure stream is at beginning
    file.file.seek(0)

    try:
        text = extract_text_from_pdf(file.file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to extract PDF text: {str(e)}")

    if not text.strip():
        raise HTTPException(status_code=204, detail="PDF has no extractable text.")

    cache_text(file.filename, text)

    return {
        "filename": file.filename,
        "status": "processed",
        "text": text[:1000]  # Return preview only
    }

@app.get("/trial/{trial_id}")
async def get_trial(trial_id: str):
    cached = get_cached_text(trial_id)
    if not cached:
        raise HTTPException(status_code=404, detail="PDF data not found in cache.")
    
    return {
        "trial_id": trial_id,
        "status": "cached",
        "text": cached[:1000]
    }

