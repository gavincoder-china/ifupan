from sqlalchemy.orm import Session
from app.entity.speech_to_text_model import SpeechToText

class SpeechToTextDAO:
    @staticmethod
    def create(db: Session, audio_file: str, prompt_type: str, transcribed_text: str, result: str):
        db_item = SpeechToText(audio_file=audio_file, prompt_type=prompt_type, transcribed_text=transcribed_text, result=result)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item

    @staticmethod
    def get_by_id(db: Session, item_id: int):
        return db.query(SpeechToText).filter(SpeechToText.id == item_id).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(SpeechToText).offset(skip).limit(limit).all()
