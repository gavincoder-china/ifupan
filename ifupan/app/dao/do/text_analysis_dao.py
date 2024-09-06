from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.entity.text_analysis_model import TextAnalysis

class TextAnalysisDAO:
    @staticmethod
    async def create(db: AsyncSession, input_text: str, prompt_type: str, result: str):
        db_item = TextAnalysis(input_text=input_text, prompt_type=prompt_type, result=result)
        db.add(db_item)
        await db.commit()
        await db.refresh(db_item)
        return db_item

    @staticmethod
    async def get_by_id(db: AsyncSession, item_id: int):
        result = await db.execute(select(TextAnalysis).filter(TextAnalysis.id == item_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100):
        result = await db.execute(select(TextAnalysis).offset(skip).limit(limit))
        return result.scalars().all()
