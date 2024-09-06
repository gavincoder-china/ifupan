from sqlalchemy.orm import Session
from ifupan.app.dao.do.speech_to_text_dao import SpeechToTextDAO
from ifupan.app.services.speech_to_text import transcribe
from ifupan.app.services.text_analysis import analyze

class SpeechToTextService:
    @staticmethod
    async def transcribe_and_analyze(db: Session, audio_file, prompt_type: str):
        transcribed_text = transcribe(audio_file)
        result = analyze(transcribed_text, prompt_type)
        return await SpeechToTextDAO.create(db, audio_file.filename, prompt_type, transcribed_text, result)

    @staticmethod
    async def get_transcription_by_id(db: Session, transcription_id: int):
        return await SpeechToTextDAO.get_by_id(db, transcription_id)

    @staticmethod
    async def get_all_transcriptions(db: Session, skip: int = 0, limit: int = 100):
        return await SpeechToTextDAO.get_all(db, skip, limit)
