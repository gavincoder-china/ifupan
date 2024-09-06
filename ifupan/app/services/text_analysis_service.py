from ifupan.app.dao.do.text_analysis_dao import TextAnalysisDAO
from sqlalchemy.orm import Session
from ifupan.app.services.text_analysis  import analyze

class TextAnalysisService:
    @staticmethod
    async def analyze_and_save(db: Session, input_text: str, prompt_type: str):
        # 这里调用您现有的分析逻辑
        result = analyze(input_text, prompt_type)
        
        # 保存结果到数据库
        return await TextAnalysisDAO.create(db, input_text, prompt_type, result)

    @staticmethod
    async def get_analysis_by_id(db: Session, analysis_id: int):
        return await TextAnalysisDAO.get_by_id(db, analysis_id)

    @staticmethod
    async def get_all_analyses(db: Session, skip: int = 0, limit: int = 100):
        return await TextAnalysisDAO.get_all(db, skip, limit)
