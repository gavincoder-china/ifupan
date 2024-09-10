from flask import Blueprint, request, jsonify
from app.services.speech_to_text_service import SpeechToTextService
from app.services.mind_map_service import MindMapService
from config.get_db import get_db

speech_to_text_bp = Blueprint('speech_to_text', __name__)

@speech_to_text_bp.route('/transcribe', methods=['POST'])
def transcribe():
    with get_db() as db:
        audio_file = request.files['audio']
        prompt_type = request.form.get('promptType', 'diary')
        generate_extras = request.form.get('generateExtras', 'false').lower() == 'true'

        result = SpeechToTextService.transcribe_and_analyze(db, audio_file, prompt_type)

        response_data = {
            'id': result['id'],
            'transcribed_text': result['transcribed_text'],
            'analysis': result['result']
        }

        if generate_extras:
            mind_map_file, pdf_file, md_file = MindMapService.generate(result['result'])
            response_data['extras'] = {
                'mind_map': mind_map_file,
                'pdf': pdf_file,
                'markdown': md_file
            }

        return jsonify(response_data)

@speech_to_text_bp.route('/<int:transcription_id>', methods=['GET'])
def get_transcription_by_id(transcription_id):
    with get_db() as db:
        result = SpeechToTextService.get_transcription_by_id(db, transcription_id)
        if result:
            return jsonify({'result': result.result})
        else:
            return jsonify({'error': 'Transcription not found'}), 404
