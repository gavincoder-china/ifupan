from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.entity.speech_to_text_model import SpeechToText

class SpeechToTextDAO:
    @staticmethod
    async def create(db: AsyncSession, audio_file: str, prompt_type: str, transcribed_text: str, result: str):
        db_item = SpeechToText(audio_file=audio_file, prompt_type=prompt_type, transcribed_text=transcribed_text, result=result)
        db.add(db_item)
        await db.commit()
        await db.refresh(db_item)
        return db_item

    @staticmethod
    async def get_by_id(db: AsyncSession, item_id: int):
        result = await db.execute(select(SpeechToText).filter(SpeechToText.id == item_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100):
        result = await db.execute(select(SpeechToText).offset(skip).limit(limit))
        return result.scalars().all()
