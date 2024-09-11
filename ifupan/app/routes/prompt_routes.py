from flask import Blueprint, jsonify, request, render_template
from app.services.prompts_service import PromptService
from config.get_db import get_db
from config.get_redis import RedisUtil

prompt_bp = Blueprint('prompt', __name__)

@prompt_bp.route('/prompts', methods=['GET'])
def get_prompts():
    with get_db() as db:
        prompts = PromptService.get_all_prompts(db)
        prompts_list = [prompt.to_dict() for prompt in prompts]
    return jsonify(prompts_list)

@prompt_bp.route('/prompts', methods=['POST'])
def create_prompt():
    data = request.json
    with get_db() as db:
        new_prompt = PromptService.create_prompt(db, data)
        return jsonify(new_prompt.to_dict()), 201

@prompt_bp.route('/prompts/<int:prompt_id>', methods=['GET'])
def get_prompt(prompt_id):
    with get_db() as db:
        prompt = PromptService.get_prompt_by_id(db, prompt_id)
        if prompt:
            return jsonify(prompt.to_dict())
        return jsonify({"error": "Prompt not found"}), 404

@prompt_bp.route('/prompts/<int:prompt_id>', methods=['PUT'])
def update_prompt(prompt_id):
    data = request.json
    with get_db() as db:
        updated_prompt = PromptService.update_prompt(db, prompt_id, data)
        if updated_prompt:
            return jsonify(updated_prompt.to_dict())
        return jsonify({"error": "Prompt not found"}), 404

@prompt_bp.route('/prompts/<int:prompt_id>', methods=['DELETE'])
def delete_prompt(prompt_id):
    with get_db() as db:
        if PromptService.delete_prompt(db, prompt_id):
            return jsonify({"message": "Prompt deleted successfully"})
        return jsonify({"error": "Prompt not found"}), 404

@prompt_bp.route('/prompt-crud')
def prompt_crud():
    return render_template('prompt_crud.html')
