from sqlalchemy.orm import Session
from app.entity.speech_to_text_model import SpeechToText

class SpeechToTextDAO:
    @staticmethod
    async def create(db: Session, audio_file: str, prompt_type: str, transcribed_text: str, result: str):
        db_item = SpeechToText(audio_file=audio_file, prompt_type=prompt_type, transcribed_text=transcribed_text, result=result)
        db.add(db_item)
        await db.commit()
        await db.refresh(db_item)
        return db_item

    @staticmethod
    async def get_by_id(db: Session, item_id: int):
        return await db.query(SpeechToText).filter(SpeechToText.id == item_id).first()

    @staticmethod
    async def get_all(db: Session, skip: int = 0, limit: int = 100):
        return await db.query(SpeechToText).offset(skip).limit(limit).all()
