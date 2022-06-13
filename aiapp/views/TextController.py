"""
    文本控制器
    @author tinaroot.cn
    @time 2022/6/10 23:06
"""
from flask import Blueprint, request
from aiapp import setting
import aiapp.utils.R as r

logger = setting.LogConfig.logger

redisUtils = setting.RedisConfig.redisClient()

bp = Blueprint('text', __name__)


@bp.route('/v1/sensitiveDetection', methods=['POST'])
def test():
    """
        敏感检测
        @author tinaroot
        @since 2022-6-10 23:10
    """
    params = request.get_json()

    return r.success_response_data(params)
