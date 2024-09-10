from sqlalchemy.orm import Session
from ifupan.app.dao.do.prompts_dao import PromptDAO
from ifupan.app.entity.prompt_model import Prompt

class PromptService:
    @staticmethod
    def get_prompt_by_code(db: Session, code: str):
        return PromptDAO.get_by_code(db, code)

    @staticmethod
    def get_all_prompts(db: Session):
        return PromptDAO.get_all(db)

    @staticmethod
    def get_prompt_by_id(db: Session, prompt_id: int):
        return PromptDAO.get_by_id(db, prompt_id)

    @staticmethod
    def create_prompt(db: Session, prompt_data: dict):
        new_prompt = Prompt(**prompt_data)
        return PromptDAO.create(db, new_prompt)

    @staticmethod
    def update_prompt(db: Session, prompt_id: int, prompt_data: dict):
        existing_prompt = PromptDAO.get_by_id(db, prompt_id)
        if existing_prompt:
            for key, value in prompt_data.items():
                setattr(existing_prompt, key, value)
            return PromptDAO.update(db, existing_prompt)
        return None

    @staticmethod
    def delete_prompt(db: Session, prompt_id: int):
        return PromptDAO.delete(db, prompt_id)
