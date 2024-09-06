from flask import Blueprint, request, jsonify, send_from_directory
from app.services.mind_map_service import MindMapService
from config.get_db import get_db
import os
import asyncio

mind_map_bp = Blueprint('mind_map', __name__)

@mind_map_bp.route('/generate', methods=['POST'])
async def generate_mind_map():
    async for db in get_db():
        data = request.json
        text = data.get('text', '')
        prompt_type = data.get('promptType', 'diary')
        
        result = await MindMapService.generate_and_save(db, text, prompt_type)
        
        return jsonify({
            'mind_map': result.mind_map_file,
            'pdf': result.pdf_file,
            'markdown': result.md_file
        })

@mind_map_bp.route('/<int:mind_map_id>', methods=['GET'])
async def get_mind_map(mind_map_id):
    async for db in get_db():
        result = await MindMapService.get_mind_map_by_id(db, mind_map_id)
        if result:
            return send_from_directory(os.path.join(os.getcwd(), 'files'), result.mind_map_file, as_attachment=True)
        else:
            return jsonify({'error': 'Mind map not found'}), 404

@mind_map_bp.route('/<int:mind_map_id>/pdf', methods=['GET'])
async def get_pdf(mind_map_id):
    async for db in get_db():
        result = await MindMapService.get_mind_map_by_id(db, mind_map_id)
        if result:
            return send_from_directory(os.path.join(os.getcwd(), 'files'), result.pdf_file, as_attachment=True)
        else:
            return jsonify({'error': 'PDF not found'}), 404

@mind_map_bp.route('/', methods=['GET'])
async def get_all_mind_maps():
    async for db in get_db():
        results = await MindMapService.get_all_mind_maps(db)
        return jsonify({'mind_maps': [{'id': r.id, 'prompt_type': r.prompt_type, 'created_at': r.created_at} for r in results]})

@mind_map_bp.route('/<path:filename>', methods=['GET'])
async def get_file(filename):
    return send_from_directory(os.path.join(os.getcwd(), 'files'), filename, as_attachment=True)
