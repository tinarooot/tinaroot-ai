from flask import Blueprint, request
from aiapp import setting
import aiapp.utils.R as r

logger = setting.LogConfig.logger

bp = Blueprint('home', __name__)


@bp.route('/v1/test', methods=['GET', 'POST'])
def test():
    print('get_json={}', request.get_json())
    print('get_data={}', request.get_data())
    print('args={}', request.args)

    return r.success_response()
