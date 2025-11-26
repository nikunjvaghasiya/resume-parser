import os
import json
from typing import Dict, Any
from loguru import logger
import openai
from openai import OpenAI
import ollama
import re

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1")

# openai.api_key = OPENAI_API_KEY


client = OpenAI(api_key="REMOVED_KEY")

SCHEMA = {
    "contact": {
        "name": "string or null",
        "email": "string or null",
        "phone": "string or null",
        "location": "string or null"
    },
    "summary": "string or null",
    "experiences": [{
        "company": "string or null",
        "role": "string or null",
        "start_date": "string or null",
        "end_date": "string or null",
        "duration": "string or null",
        "responsibilities": ["string"]
    }],
    "education": [{
        "degree": "string or null",
        "institution": "string or null",
        "start_year": "string or null",
        "end_year": "string or null"
    }],
    "skills": ["string"],
    "certifications": ["string"]
}

PROMPT_TEMPLATE = """
You are a resume parsing assistant.
Extract the following fields from the resume text and output JSON EXACTLY matching the schema.

Schema:
{schema}

Instructions:
- Only output valid JSON and nothing else.
- If a field is not present, output null (for strings) or empty list (for arrays).
- Try to normalize dates to YYYY or YYYY-MM format when possible, otherwise return the raw text.
- For experiences and education, include multiple entries if present.
- Provide responsibilities as an array of short strings.

Resume Text:
\"\"\"{text}\"\"\"
"""

def build_prompt(text: str) -> str:
    return PROMPT_TEMPLATE.format(schema=json.dumps(SCHEMA, indent=2), text=text[:15000])  # truncate large docs

def parse_resume_with_openai(text: str) -> Dict[str, Any]:
    prompt = build_prompt(text)
    logger.debug("Sending prompt to OpenAI")
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role":"system","content":"You extract structured resume info."},
                  {"role":"user","content":prompt}],
        temperature=0.0,
        max_tokens=2000
    )
    content = resp.choices[0].message.content
    # The model should return JSON. Wrap in try/except parse.
    try:
        parsed = json.loads(content)
    except Exception as e:
        logger.error("Failed to parse JSON from LLM response: %s", e)
        # attempt to salvage with simple heuristics (strip leading/trailing text)
        import re
        m = re.search(r"\{.*\}", content, re.DOTALL)
        if m:
            parsed = json.loads(m.group(0))
        else:
            raise RuntimeError("LLM did not return valid JSON")
    return parsed

def parse_resume_with_ollama(text: str) -> Dict[str, Any]:
    from app.services.llm_service import build_prompt  
    prompt = build_prompt(text)

    try:
        response = ollama.chat(
            model="mistral",
            messages=[
                {"role": "system", "content": "You extract structured resume info."},
                {"role": "user", "content": prompt}
            ]
        )
    except Exception as e:
        logger.error(f"Ollama Error: {e}")
        raise

    content = response["message"]["content"]

    try:
        return json.loads(content)
    except:
        match = re.search(r"\{.*\}", content, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        raise RuntimeError(f"Invalid JSON: {content}")
