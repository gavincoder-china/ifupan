from flask import Blueprint, jsonify
from app.services.prompts_service import PromptService
from config.get_db import get_db
from config.get_redis import RedisUtil

common_bp = Blueprint('common', __name__)

@common_bp.route('/prompts', methods=['GET'])
async def get_prompts():
    redis = await RedisUtil.create_redis_pool()
    cached_prompts = await redis.get('prompts_list')

    if cached_prompts:
        await RedisUtil.close_redis_pool(redis)
        return jsonify(eval(cached_prompts))
    
    async for db in get_db():
        prompts = await PromptService.get_all_prompts(db)
    
        prompts_list = [{'code': p.code, 'name': p.name} for p in prompts]
        await redis.set('prompts_list', str(prompts_list), ex=3600)  # Cache for 1 hour
    
    await RedisUtil.close_redis_pool(redis)
    return jsonify(prompts_list)
