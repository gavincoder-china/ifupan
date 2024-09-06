from sqlalchemy.orm import Session
from sqlalchemy.future import select
from app.entity.prompt_model import Prompt

class PromptDAO:
    @staticmethod
    async def get_by_code(db: Session, code: str):
        result = await db.execute(select(Prompt).filter(Prompt.code == code))
        return result.scalars().first()

    @staticmethod
    async def get_all(db: Session):
        result = await db.execute(select(Prompt))
        return result.scalars().all()
