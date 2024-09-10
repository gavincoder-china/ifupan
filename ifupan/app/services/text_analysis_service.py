from ifupan.app.dao.do.text_analysis_dao import TextAnalysisDAO
from sqlalchemy.orm import Session
from ifupan.utils.deepseek_v2_langchain import deepseek_analyze
from ifupan.app.services.prompts_service import PromptService
from config.get_redis import RedisUtil

class TextAnalysisService:
    @staticmethod
    def analyze_and_save(db: Session, input_text: str, prompt_type: str):
        result = TextAnalysisService.analyze(db, input_text, prompt_type)
        return TextAnalysisDAO.create(db, input_text, prompt_type, result)

    @staticmethod
    def get_analysis_by_id(db: Session, analysis_id: int):
        return TextAnalysisDAO.get_by_id(db, analysis_id)

    @staticmethod
    def get_all_analyses(db: Session, skip: int = 0, limit: int = 100):
        return TextAnalysisDAO.get_all(db, skip, limit)

    @staticmethod
    def analyze(db: Session, text: str, prompt_type: str):
        redis = RedisUtil.create_redis_pool_sync()
        cached_prompt = redis.get(f'prompt:{prompt_type}')

        if cached_prompt:
            task_description = cached_prompt if isinstance(cached_prompt, str) else cached_prompt.decode('utf-8')
        else:
            prompt = PromptService.get_prompt_by_code(db, prompt_type)
            if prompt:
                task_description = prompt.content
                redis.set(f'prompt:{prompt_type}', task_description, ex=3600)  # Cache for 1 hour
            else:
                # Fallback to default prompt if not found
                task_description = "Please provide a detailed analysis of the given text."

        RedisUtil.close_redis_pool_sync(redis)
        result = deepseek_analyze(text, task_description)
        return result
