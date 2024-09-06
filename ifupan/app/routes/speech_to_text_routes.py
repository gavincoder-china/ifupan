from flask import Blueprint, request, jsonify
from app.services.speech_to_text_service import SpeechToTextService
from app.services.mind_map_service import MindMapService
from config.get_db import get_db
import asyncio

speech_to_text_bp = Blueprint('speech_to_text', __name__)

@speech_to_text_bp.route('/transcribe', methods=['POST'])
async def transcribe():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    
    audio_file = request.files['audio']
    prompt_type = request.form.get('promptType', 'diary')
    generate_extras = request.form.get('generateExtras', 'false').lower() == 'true'
    
    async with get_db() as db:
        result = await SpeechToTextService.transcribe_and_analyze(db, audio_file, prompt_type)
        
        response_data = {'result': result.result}
        
        if generate_extras:
            mind_map_file, pdf_file, md_file = await MindMapService.generate(result.result)
            response_data['extras'] = {
                'mind_map': mind_map_file,
                'pdf': pdf_file,
                'markdown': md_file
            }
        
        return jsonify(response_data)

@speech_to_text_bp.route('/<int:transcription_id>', methods=['GET'])
async def get_transcription(transcription_id):
    async with get_db() as db:
        result = await SpeechToTextService.get_transcription_by_id(db, transcription_id)
        if result:
            return jsonify({'result': result.result})
        else:
            return jsonify({'error': 'Transcription not found'}), 404
