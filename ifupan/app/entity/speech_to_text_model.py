from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from config.database import Base

class SpeechToText(Base):
    __tablename__ = "speech_to_text"

    id = Column(Integer, primary_key=True, index=True)
    audio_file = Column(String(255), nullable=False)
    prompt_type = Column(String(50), nullable=False)
    transcribed_text = Column(Text, nullable=False)
    result = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
