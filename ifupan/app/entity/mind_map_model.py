from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from config.database import Base

class MindMap(Base):
    __tablename__ = "mind_map"

    id = Column(Integer, primary_key=True, index=True)
    input_text = Column(Text, nullable=False)
    prompt_type = Column(String(50), nullable=False)
    mind_map_file = Column(String(255), nullable=False)
    pdf_file = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
