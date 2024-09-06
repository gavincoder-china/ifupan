from sqlalchemy.orm import Session
from ifupan.app.dao.do.prompts_dao import PromptDAO

class PromptService:
    @staticmethod
    async def get_prompt_by_code(db: Session, code: str):
        return await PromptDAO.get_by_code(db, code)

    @staticmethod
    async def get_all_prompts(db: Session):
        return await PromptDAO.get_all(db)
