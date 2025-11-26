import fitz
from docx import Document
from typing import Optional
from pathlib import Path
from loguru import logger

def extract_text_from_pdf(path: Path) -> str:
    logger.debug(f"Extracting PDf text from {path}")

    doc = fitz.open(path)
    text_chunks = []
    for page in doc:
        text = page.get_text("text")
        if text:
            text_chunks.append(text)
    
    return "\n".join(text_chunks)

def extract_text_from_docx(path: Path) -> str:
    logger.debug(f"Extracting DOCX text from {path}")
    doc = Document(path)
    paragraphs = [p.text for p in doc.paragraphs if p.text and p.text.strip()]
    return "\n".join(paragraphs)

def extract_text(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return extract_text_from_pdf(path)
    elif suffix in {".doc", ".docx"}:
        return extract_text_from_docx(path) 
    else:
        raise ValueError("Unsupported file type!")