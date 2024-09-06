from sqlalchemy.orm import Session
from ifupan.app.dao.do.speech_to_text_dao import SpeechToTextDAO
from ifupan.app.services.text_analysis_service import TextAnalysisService
import os
import uuid
import assemblyai as aai
from opencc import OpenCC
from dotenv import load_dotenv

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
    async def transcribe_and_analyze(db: Session, audio_file, prompt_type: str):
        transcribed_text = SpeechToTextService.transcribe(audio_file)
        result = await TextAnalysisService.analyze(db, transcribed_text, prompt_type)
        return await SpeechToTextDAO.create(db, audio_file.filename, prompt_type, transcribed_text, result)

    @staticmethod
    async def get_transcription_by_id(db: Session, transcription_id: int):
        return await SpeechToTextDAO.get_by_id(db, transcription_id)

    @staticmethod
    async def get_all_transcriptions(db: Session, skip: int = 0, limit: int = 100):
        return await SpeechToTextDAO.get_all(db, skip, limit)

    @staticmethod
    def detect_language(audio_url):
        config = aai.TranscriptionConfig(
            audio_end_at=60000,
            language_detection=True,
            speech_model=aai.SpeechModel.nano,
        )
        transcript = transcriber.transcribe(audio_url, config=config)
        return transcript.json_response["language_code"]

    @staticmethod
    def transcribe_file(audio_url, language_code):
        config = aai.TranscriptionConfig(
            language_code=language_code,
            speech_model=(
                aai.SpeechModel.best
                if language_code in supported_languages_for_best
                else aai.SpeechModel.nano
            ),
        )
        transcript = transcriber.transcribe(audio_url, config=config)
        return transcript

    @staticmethod
    def asr(audio_url):
        language_code = SpeechToTextService.detect_language(audio_url)
        transcript = SpeechToTextService.transcribe_file(audio_url, language_code)

        if language_code in ['zh', 'zh-TW', 'zh-HK']:
            cc = OpenCC('t2s')
            return cc.convert(transcript.text)
        else:
            return transcript.text

    @staticmethod
    def transcribe(audio_file):
        # Save the uploaded file temporarily
        temp_filename = f"audio/{uuid.uuid4()}.wav"
        audio_file.save(temp_filename)

        # Detect language
        language_code = SpeechToTextService.detect_language(temp_filename)

        # Transcribe the file
        transcript = SpeechToTextService.transcribe_file(temp_filename, language_code)

        # Remove the temporary file
        os.remove(temp_filename)

        # Convert simplified Chinese to traditional Chinese if needed
        if language_code == "zh":
            cc = OpenCC('s2t')
            return cc.convert(transcript.text)
        else:
            return transcript.text
