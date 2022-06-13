import os

from flask import Flask, request, json
from flask_cors import CORS

import aiapp.utils.R as r

from aiapp import views
from aiapp import setting

logger = setting.LogConfig.logger

current_dir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
urlPrefix = '/aiapp/'

app.register_blueprint(views.HomeController.bp, url_prefix=urlPrefix)
app.register_blueprint(views.TextController.bp, url_prefix=urlPrefix + 'text')
app.register_blueprint(views.MoodController.bp, url_prefix=urlPrefix)

rules = [str(p) for p in app.url_map.iter_rules()]
logger.info(f"可用的访问路由: rules = 【{rules}】")


@app.errorhandler(Exception)
def all_exception_handler(e):
    logger.info("全局异常={},状态码={},类型={}", e, e.code, type(e))
    return r.code_response(e.code)


# 解决跨域问题
# CORS(app , supports_credentials = True)
CORS(app)


@app.before_request
def first_request():
    """
    token 验证
    :return:
    """
    params = request.get_json()
    logger.info(params)


if __name__ == '__main__':
    port = 8080
    app.run(host="0.0.0.0", port=port, threaded=True)
