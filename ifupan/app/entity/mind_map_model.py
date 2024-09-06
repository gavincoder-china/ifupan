from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from config.database import Base
from datetime import datetime

class MindMap(Base):
    __tablename__ = "mind_map"

    id = Column(Integer, primary_key=True, index=True)
    input_text = Column(String)
    prompt_type = Column(String)
    mind_map_file = Column(String)
    pdf_file = Column(String)
    md_file = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
