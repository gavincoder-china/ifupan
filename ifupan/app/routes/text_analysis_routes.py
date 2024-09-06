from flask import Blueprint, request, jsonify
from app.services.text_analysis_service import TextAnalysisService
from config.get_db import get_db

text_analysis_bp = Blueprint('text_analysis', __name__)

@text_analysis_bp.route('/analyze', methods=['POST'])
async def analyze():
    async for db in get_db():
        data = request.json
        text = data.get('text', '')
        prompt_type = data.get('promptType', 'diary')
        
        result = await TextAnalysisService.analyze_and_save(db, text, prompt_type)
        
        return jsonify({'result': result.result})

@text_analysis_bp.route('/<int:analysis_id>', methods=['GET'])
async def get_analysis_by_id(analysis_id):
    async for db in get_db():
        result = await TextAnalysisService.get_analysis_by_id(db, analysis_id)
        if result:
            return jsonify({'result': result.result})
        else:
            return jsonify({'error': 'Analysis not found'}), 404

@text_analysis_bp.route('/', methods=['GET'])
async def get_all_analyses():
    async for db in get_db():
        skip = request.args.get('skip', 0, type=int)
        limit = request.args.get('limit', 100, type=int)
        results = await TextAnalysisService.get_all_analyses(db, skip, limit)
        return jsonify({'analyses': [{'id': r.id, 'prompt_type': r.prompt_type, 'created_at': r.created_at} for r in results]})