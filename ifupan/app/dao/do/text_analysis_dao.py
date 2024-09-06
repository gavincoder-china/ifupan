from sqlalchemy.orm import Session
from app.entity.text_analysis_model import TextAnalysis

class TextAnalysisDAO:
    @staticmethod
    async def create(db: Session, input_text: str, prompt_type: str, result: str):
        db_item = TextAnalysis(input_text=input_text, prompt_type=prompt_type, result=result)
        db.add(db_item)
        await db.commit()
        await db.refresh(db_item)
        return db_item

    @staticmethod
    async def get_by_id(db: Session, item_id: int):
        return await db.query(TextAnalysis).filter(TextAnalysis.id == item_id).first()

    @staticmethod
    async def get_all(db: Session, skip: int = 0, limit: int = 100):
        return await db.query(TextAnalysis).offset(skip).limit(limit).all()
