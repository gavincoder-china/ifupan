from sqlalchemy.orm import Session
from ifupan.app.dao.do.prompts_dao import PromptDAO

class PromptService:
    @staticmethod
    def get_prompt_by_code(db: Session, code: str):
        return PromptDAO.get_by_code(db, code)

    @staticmethod
    def get_all_prompts(db: Session):
        return PromptDAO.get_all(db)
