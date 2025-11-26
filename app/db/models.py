from sqlalchemy import Column, String, Text, DateTime, Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    document_id = Column(String, unique=True)
    filename = Column(String)
    file_path = Column(String)
    raw_text = Column(JSONB)
    parsed_json = Column(JSONB)
    created_at = Column(DateTime, server_default=func.now())

