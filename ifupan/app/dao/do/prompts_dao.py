from sqlalchemy.orm import Session
from app.entity.prompt_model import Prompt

class PromptDAO:
    @staticmethod
    async def get_by_code(db: Session, code: str):
        return await db.query(Prompt).filter(Prompt.code == code).first()

    @staticmethod
    async def get_all(db: Session):
        return await db.query(Prompt).all()
