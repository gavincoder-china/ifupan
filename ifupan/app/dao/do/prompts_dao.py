from sqlalchemy.orm import Session
from sqlalchemy.future import select
from app.entity.prompt_model import Prompt

class PromptDAO:
    @staticmethod
    def get_by_code(db: Session, code: str):
        result = db.execute(select(Prompt).filter(Prompt.code == code))
        return result.scalars().first()

    @staticmethod
    def get_all(db: Session):
        result = db.execute(select(Prompt))
        return result.scalars().all()
