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

    @staticmethod
    def get_by_id(db: Session, prompt_id: int):
        result = db.execute(select(Prompt).filter(Prompt.id == prompt_id))
        return result.scalars().first()

    @staticmethod
    def create(db: Session, prompt: Prompt):
        db.add(prompt)
        db.commit()
        db.refresh(prompt)
        return prompt

    @staticmethod
    def update(db: Session, prompt: Prompt):
        db.commit()
        db.refresh(prompt)
        return prompt

    @staticmethod
    def delete(db: Session, prompt_id: int):
        prompt = PromptDAO.get_by_id(db, prompt_id)
        if prompt:
            db.delete(prompt)
            db.commit()
            return True
        return False
