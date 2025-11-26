# Resume Parser

Resume Parser — FastAPI backend + Streamlit UI that extracts structured resume fields using a local Ollama LLM (Mistral).  
This project stores files and parsed JSON in PostgreSQL (async SQLAlchemy + Alembic).

---

## Features
- Upload PDF/DOCX resumes via Streamlit or API
- Extract structured fields (contact, summary, skills, experience) using a local Ollama model (Mistral)
- Store resume file metadata + parsed JSON in PostgreSQL (JSONB)
- Async FastAPI endpoints + Alembic migrations
- List/process resumes and view parsed content from the UI

---

## Prerequisites (local dev)
- Python 3.10+ (3.11/3.12 recommended)
- PostgreSQL (running locally)
- [Ollama](https://ollama.com/) installed for local LLM inference
- (Optional) Git & GitHub account

---

## Setup

### 1. Clone & create virtualenv
```bash
git clone https://github.com/nikunjvaghasiya/resume-parser.git
cd resume-parser
python -m venv .venv
source .venv/bin/activate

# 2.Install Python dependencies
pip install -r requirements.txt

#3. Setup PostgreSQL database
sudo -u postgres psql
CREATE DATABASE resume_db;
CREATE USER resume_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE resume_db TO resume_user;
\q

#4. Install Ollama and pull Mistral
Install Ollama (see https://ollama.com/docs/):

# Linux example
curl -fsSL https://ollama.com/install.sh | sh
# Pull a Mistral model (recommended small/quantized flavor if low memory)
ollama pull mistral
# or use a quantized variant if available: ollama pull mistral:7b-instruct-q4_0


#5. Initialize DB schema (Alembic)
# Ensure env.py is configured to use your DATABASE_URL and target metadata
alembic revision --autogenerate -m "initial"
alembic upgrade head

# 6. Run the backend and UI
Start FastAPI:
uvicorn app.main:app --reload --port 8000

Start Streamlit UI:
streamlit run ui/streamlit_app.py

API Endpoints

POST /api/upload — upload a resume (multipart/form-data: file)
GET /api/resume/{document_id} — fetch parsed resume
GET /api/resumes — list processed resumes
GET /api/file/{document_id} — download original file