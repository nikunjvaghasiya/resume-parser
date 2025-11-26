from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import date

class ContactInfo(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[str]
    location: Optional[str]

class JobEntry(BaseModel):
    company: Optional[str]
    role: Optional[str]
    start_date: Optional[str]
    end_date: Optional[str]
    duration: Optional[str]
    responsibilities: Optional[List[str]] = []

class EducationEntry(BaseModel):
    degree: Optional[str]
    institution: Optional[str]
    start_year: Optional[str]
    end_year: Optional[str]

class ResumeParseResult(BaseModel):
    document_id: str
    contact: ContactInfo
    summary: Optional[str]
    experiences: List[JobEntry] = []
    education: List[EducationEntry] = []
    skills: List[str] = []
    certifications = List[str] = []
    raw_text: Optional[str] = None

    