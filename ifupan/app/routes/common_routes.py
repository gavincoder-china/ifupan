from flask import Blueprint, jsonify
from app.services.prompts_service import PromptService
from config.get_db import get_db
from config.get_redis import RedisUtil

common_bp = Blueprint('common', __name__)

@common_bp.route('/prompts', methods=['GET'])
def get_prompts():
    redis = RedisUtil.create_redis_pool_sync()
    cached_prompts = redis.get('prompts_list')

    if cached_prompts:
        RedisUtil.close_redis_pool_sync(redis)
        try:
            return jsonify(eval(cached_prompts.decode('utf-8') if isinstance(cached_prompts, bytes) else cached_prompts))
        except:
            # If there's an error decoding or evaluating the cached data, we'll fetch fresh data
            pass

    with get_db() as db:
        prompts = PromptService.get_all_prompts(db)
    
        prompts_list = [{'code': p.code, 'name': p.name} for p in prompts]
        redis.set('prompts_list', str(prompts_list), ex=3600)  # Cache for 1 hour
    
    RedisUtil.close_redis_pool_sync(redis)
    return jsonify(prompts_list)
