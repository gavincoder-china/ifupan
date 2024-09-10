from sqlalchemy.orm import Session
from app.entity.text_analysis_model import TextAnalysis

class TextAnalysisDAO:
    @staticmethod
    def create(db: Session, input_text: str, prompt_type: str, result: str):
        db_item = TextAnalysis(input_text=input_text, prompt_type=prompt_type, result=result)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item

    @staticmethod
    def get_by_id(db: Session, item_id: int):
        return db.query(TextAnalysis).filter(TextAnalysis.id == item_id).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(TextAnalysis).offset(skip).limit(limit).all()
