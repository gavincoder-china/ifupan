# https://www.assemblyai.com/app 免费额度

import os
import uuid
import assemblyai as aai
from opencc import OpenCC
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()
# 获取环境变量

aai.settings.api_key = os.getenv("assemblyai_stt")

transcriber = aai.Transcriber()

supported_languages_for_best = {
    "en",
    "es",
    "fr",
    "de",
    "it",
    "pt",
    "nl",
    "hi",
    "ja",
    "zh",
    "fi",
    "ko",
    "pl",
    "ru",
    "tr",
    "uk",
    "vi",
}

# Create an 'audio' directory if it doesn't exist
if not os.path.exists('audio'):
    os.makedirs('audio')

def detect_language(audio_url):
    config = aai.TranscriptionConfig(
        audio_end_at=60000,  # first 60 seconds (in milliseconds)
        language_detection=True,
        speech_model=aai.SpeechModel.nano,
    )
    transcript = transcriber.transcribe(audio_url, config=config)
    return transcript.json_response["language_code"]


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


def asr(audio_url):
    language_code = detect_language(audio_url)
    transcript = transcribe_file(audio_url, language_code)

    # 如果检测到的语言是中文，则进行繁体到简体的转换
    if language_code in ['zh', 'zh-TW', 'zh-HK']:
        cc = OpenCC('t2s')  # 繁体到简体
        return cc.convert(transcript.text)
    else:
        return transcript.text


## ASR转换文字，这边需要做一个转换音频文件为文字的功能，whisper是可以用的
def transcribe(audio_file):
    # Generate a unique filename
    unique_filename = f"{uuid.uuid4()}.wav"
    file_path = os.path.join('audio', unique_filename)

    # Save the audio file
    audio_file.save(file_path)

    result = asr(file_path)
    return result
