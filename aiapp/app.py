import os

from flask import Flask, request
from flask_cors import CORS

import aiapp.utils.R as r
import aiapp.utils.LogUtils as logUtils

from aiapp import views
from aiapp import setting

logger = setting.LogConfig.logger
redisUtils = setting.RedisConfig.redisClient()

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
    logUtils.errorLog(e)
    return r.code_response(e.code)


# 解决跨域问题
# CORS(app , supports_credentials = True)
CORS(app)


@app.before_request
def first_request():
    """
    请求记录
    :return:
    """
    params = request.get_json()
    logger.info(params)

    platform = request.user_agent.platform if request.user_agent.platform else 'unknown'
    browser = request.user_agent.browser if request.user_agent.browser else 'unknown' + request.user_agent.version if request.user_agent.version else 'unknown'
    ipaddr = request.headers.get('X-Forwarded-For', request.remote_addr) if request.headers.get('X-Forwarded-For',
                                                                                                request.remote_addr) else 'unknown'
    path = request.path
    method = request.method

    if request.method == "POST":
        reqData = request.get_json()
        logger.debug('全局请求参数POST:{}', reqData)
        logUtils.recordAccess(platform, browser, ipaddr, path, reqData, method)
    elif request.method == "GET":
        reqData = request.args
        logUtils.recordAccess(platform, browser, ipaddr, path, reqData, method)
        logger.debug('全局请求参数GET:{}', reqData)
    else:
        logger.info("错误请求方式:{}", request.method)
        logUtils.recordAccess(platform, browser, ipaddr, path, None, method)
        return r.method_error()


if __name__ == '__main__':
    port = 8080
    app.run(host="0.0.0.0", port=port, threaded=True)
