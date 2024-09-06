from ifupan.app.dao.do.text_analysis_dao import TextAnalysisDAO
from sqlalchemy.orm import Session
from ifupan.utils.deepseek_v2_langchain import deepseek_analyze
from ifupan.app.services.prompt_fupan import fupan_prompts

class TextAnalysisService:
    @staticmethod
    async def analyze_and_save(db: Session, input_text: str, prompt_type: str):
        result = TextAnalysisService.analyze(input_text, prompt_type)
        return await TextAnalysisDAO.create(db, input_text, prompt_type, result)

    @staticmethod
    async def get_analysis_by_id(db: Session, analysis_id: int):
        return await TextAnalysisDAO.get_by_id(db, analysis_id)

    @staticmethod
    async def get_all_analyses(db: Session, skip: int = 0, limit: int = 100):
        return await TextAnalysisDAO.get_all(db, skip, limit)

    @staticmethod
    def analyze(text, prompt_type):
        task_description = fupan_prompts.get(prompt_type, fupan_prompts['diary'])
        result = deepseek_analyze(text, task_description)
        return result
