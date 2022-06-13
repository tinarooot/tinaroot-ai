"""
    日志封装工具类
   @author TinaRoot
   @since 2022/6/13 下午3:59
"""
import time
import json

from aiapp import setting

logger = setting.LogConfig.logger
redisUtils = setting.RedisConfig.redisClient()


def recordAccess(platform, browser, ipaddr, path, reqData, requestMethod):
    """
     记录访问日志
    request.path: /test/a
    request.host: 127.0.0.1:5000
    request.host_url: http://127.0.0.1:5000/
    request.full_path: /test/a?x=1
    request.script_root:
    request.url: http://127.0.0.1:5000/test/a?x=1
    request.base_url: http://127.0.0.1:5000/test/a
    request.url_root: http://127.0.0.1:5000/
    :return:
    """
    # print(request.headers.get('User-Agent'))
    # 客户端操作系统

    getTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    if '127.0.0.1' != ipaddr:
        data = {
            'browser': browser,
            'os': platform,
            'ip': ipaddr,
            'uri': path,
            'time': getTime,
            'msg': 'tina-py',
            'data': reqData,
            'requestMethod': requestMethod
        }
        key = 'access_log'
        parm = json.dumps(data)
        redisUtils.lpush(key, parm)


def errorLog(e):
    """
    错误日志记录
    """
    logger.info('错误日志记录:{}', e)
    key = 'error_log'
    data = {
        'e': e,
        'code': e.code,
        'type': type(e)
    }
    parm = json.dumps(data)
    redisUtils.lpush(key, parm)
