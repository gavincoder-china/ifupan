from sqlalchemy.ext.asyncio import AsyncSession
from ifupan.app.dao.do.speech_to_text_dao import SpeechToTextDAO
from ifupan.app.services.text_analysis_service import TextAnalysisService
import os
import uuid
import assemblyai as aai
from opencc import OpenCC
from dotenv import load_dotenv
import asyncio

load_dotenv()

aai.settings.api_key = os.getenv("assemblyai_stt")
transcriber = aai.Transcriber()

supported_languages_for_best = {
    "en", "es", "fr", "de", "it", "pt", "nl", "hi", "ja", "zh",
    "fi", "ko", "pl", "ru", "tr", "uk", "vi",
}

if not os.path.exists('audio'):
    os.makedirs('audio')

class SpeechToTextService:
    @staticmethod
    async def transcribe_and_analyze(db: AsyncSession, audio_file, prompt_type: str):
        transcribed_text = await SpeechToTextService.transcribe(audio_file)
        result = await TextAnalysisService.analyze(db, transcribed_text, prompt_type)
        created_record = await SpeechToTextDAO.create(db, audio_file.filename, prompt_type, transcribed_text, result)
        return {
            'id': created_record.id,
            'transcribed_text': created_record.transcribed_text,
            'result': created_record.result
        }

    @staticmethod
    async def get_transcription_by_id(db: AsyncSession, transcription_id: int):
        return await SpeechToTextDAO.get_by_id(db, transcription_id)

    @staticmethod
    async def get_all_transcriptions(db: AsyncSession, skip: int = 0, limit: int = 100):
        return await SpeechToTextDAO.get_all(db, skip, limit)

    @staticmethod
    async def detect_language(audio_url):
        config = aai.TranscriptionConfig(
            audio_end_at=60000,
            language_detection=True,
            speech_model=aai.SpeechModel.nano,
        )
        transcript = await asyncio.to_thread(transcriber.transcribe, audio_url, config=config)
        return transcript.json_response["language_code"]

    @staticmethod
    async def transcribe_file(audio_url, language_code):
        config = aai.TranscriptionConfig(
            language_code=language_code,
            speech_model=(
                aai.SpeechModel.best
                if language_code in supported_languages_for_best
                else aai.SpeechModel.nano
            ),
        )
        transcript = await asyncio.to_thread(transcriber.transcribe, audio_url, config=config)
        return transcript.text

    @staticmethod
    async def transcribe(audio_file):
        filename = f"{uuid.uuid4()}.wav"
        file_path = os.path.join('audio', filename)
        audio_file.save(file_path)

        language_code = await SpeechToTextService.detect_language(file_path)
        transcribed_text = await SpeechToTextService.transcribe_file(file_path, language_code)

        os.remove(file_path)

        if language_code.startswith('zh'):
            cc = OpenCC('s2t')
            transcribed_text = cc.convert(transcribed_text)

        return transcribed_text
