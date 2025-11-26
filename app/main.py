from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
import os
from loguru import logger
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.services.parser import extract_text
from app.services.llm_service import parse_resume_with_openai, parse_resume_with_ollama
from app.db.models import Resume
from sqlalchemy import select



UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "./data/uploads"))
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


app = FastAPI()

app.middleware(
    CORSMiddleware,

)

@app.post("/api/upload")
async def upload_resume(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    suffix = Path(file.filename).suffix.lower()
    if suffix not in {".pdf", ".doc", ".docx"}:
        raise HTTPException(status_code=400, detail="Unsupported file type.")
    
    doc_id = str(uuid.uuid4())
    dest = UPLOAD_DIR / f"{doc_id}{suffix}"
    contents = await file.read()
    dest.write_bytes(contents)

    try:
        raw_text = extract_text(dest)
        print("raw text: ", raw_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Text extraction failed: {e}")


    try:
        parsed_json = parse_resume_with_ollama(raw_text)
        print("parsed json: ", parsed_json)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM JSON parse error: {str(e)}")

    resume_entry = Resume(
        document_id=doc_id,
        filename=file.filename,
        file_path=str(dest),
        raw_text=raw_text,
        parsed_json=parsed_json 
    )

    db.add(resume_entry)
    await db.commit()
    await db.refresh(resume_entry)

    return {
        "document_id": doc_id,
        "message": "Resume uploaded and parsed successfully",
        "parsed_data": parsed_json
    }


@app.get("/api/resumes")
async def list_resumes(db: AsyncSession = Depends(get_db)):
    query = select(Resume).order_by(Resume.created_at.desc())
    result = await db.execute(query)
    resumes = result.scalars().all()

    return [
        {
            "id": r.id,
            "document_id": r.document_id,
            "filename": r.filename,
            "created_at": r.created_at,
            "file_path": r.file_path,
        }
        for r in resumes
    ]

@app.get("/api/resume/{document_id}")
async def get_resume(document_id: str, db: AsyncSession = Depends(get_db)):
    query = select(Resume).where(Resume.document_id == document_id)
    result = await db.execute(query)
    resume = result.scalar_one_or_none()

    if not resume:
        raise HTTPException(status_code=400, detail="Resume not found")
    
    return {
        "document_id": resume.document_id,
        "filename": resume.filename,
        "file_path": resume.file_path,
        "raw_text": resume.raw_text,
        "parsed_json": resume.parsed_json
    }