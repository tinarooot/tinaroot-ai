"""
    情绪分析
   @author TinaRoot
   @since 2022/6/13 下午3:07
"""

from flask import Blueprint, request

import aiapp.utils.R as r
import aiapp.reasoning.MoodReasoning as mood
from aiapp import setting

logger = setting.LogConfig.logger

bp = Blueprint('mood', __name__)


@bp.route('/v1/mood', methods=['POST'])
def test():
    """
        情绪推理接口
    """
    param = request.get_json()

    txt = param.get('txt')
    if txt is None:
        return r.missingParam()

    result = mood.mood(txt)

    return r.success_response_data(result)
