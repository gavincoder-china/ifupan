from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from config.database import Base

class TextAnalysis(Base):
    __tablename__ = "text_analysis"

    id = Column(Integer, primary_key=True, index=True)
    input_text = Column(Text, nullable=False)
    prompt_type = Column(String(50), nullable=False)
    result = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
