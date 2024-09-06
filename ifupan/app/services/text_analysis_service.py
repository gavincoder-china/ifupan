from ifupan.app.dao.do.text_analysis_dao import TextAnalysisDAO
from sqlalchemy.orm import Session
from ifupan.utils.deepseek_v2_langchain import deepseek_analyze
from ifupan.app.services.prompts_service import PromptService
from config.get_redis import RedisUtil

class TextAnalysisService:
    @staticmethod
    async def analyze_and_save(db: Session, input_text: str, prompt_type: str):
        result = await TextAnalysisService.analyze(db, input_text, prompt_type)
        return await TextAnalysisDAO.create(db, input_text, prompt_type, result)

    @staticmethod
    async def get_analysis_by_id(db: Session, analysis_id: int):
        return await TextAnalysisDAO.get_by_id(db, analysis_id)

    @staticmethod
    async def get_all_analyses(db: Session, skip: int = 0, limit: int = 100):
        return await TextAnalysisDAO.get_all(db, skip, limit)

    @staticmethod
    async def analyze(db: Session, text: str, prompt_type: str):
        redis = await RedisUtil.create_redis_pool()
        cached_prompt = await redis.get(f'prompt:{prompt_type}')

        if cached_prompt:
            task_description = cached_prompt
        else:
            prompt = await PromptService.get_prompt_by_code(db, prompt_type)
            if prompt:
                task_description = prompt.content
                await redis.set(f'prompt:{prompt_type}', task_description, ex=3600)  # Cache for 1 hour
            else:
                # Fallback to default prompt if not found
                task_description = "Please provide a detailed analysis of the given text."

        await RedisUtil.close_redis_pool(redis)
        result = deepseek_analyze(text, task_description)
        return result
