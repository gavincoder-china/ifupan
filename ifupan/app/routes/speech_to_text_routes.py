from flask import Blueprint, request, jsonify
from app.services.speech_to_text_service import SpeechToTextService
from config.get_db import get_db

speech_to_text_bp = Blueprint('speech_to_text', __name__)

@speech_to_text_bp.route('/transcribe', methods=['POST'])
async def transcribe():
    async for db in get_db():
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        audio_file = request.files['audio']
        prompt_type = request.form.get('promptType', 'diary')
        
        result = await SpeechToTextService.transcribe_and_analyze(db, audio_file, prompt_type)
        
        return jsonify({'result': result.result})

@speech_to_text_bp.route('/<int:transcription_id>', methods=['GET'])
async def get_transcription(transcription_id):
    async for db in get_db():
        result = await SpeechToTextService.get_transcription_by_id(db, transcription_id)
        if result:
            return jsonify({'result': result.result})
        else:
            return jsonify({'error': 'Transcription not found'}), 404

@speech_to_text_bp.route('/', methods=['GET'])
async def get_all_transcriptions():
    async for db in get_db():
        skip = request.args.get('skip', 0, type=int)
        limit = request.args.get('limit', 100, type=int)
        results = await SpeechToTextService.get_all_transcriptions(db, skip, limit)
        return jsonify({'transcriptions': [{'id': r.id, 'prompt_type': r.prompt_type, 'created_at': r.created_at} for r in results]})
