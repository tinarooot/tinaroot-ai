"""
    返回JSON格式自定义类

   @author TinaRoot
   @since 2022/4/25 下午2:33
"""


def success_response():
    return {"code": 200, "msg": '操作成功'}


def to_success_response(data):
    print(data)
    if data.get('flag'):
        return success_response_data(data.get('data'))
    else:
        return fail_response_data(data.get('data'))


def success_response_msg(msg):
    return {"code": 200, "msg": msg}


def success_response_data(data):
    return {"code": 200, "msg": '请求成功', 'data': data}


def success_response_msg_data(msg, data):
    return {"code": 200, "msg": msg, 'data': data}


def fail_response():
    return {"code": 100, "msg": '请求失败'}


def fail_response_msg(msg):
    return {"code": 100, "msg": msg}


def fail_response_data(data):
    return {"code": 100, "msg": '请求失败', "data": data}


def fail_response_msg_data(msg, data):
    return {"code": 100, "msg": msg, "data": data}


def param_error_response():
    return {"code": 400, "msg": "参数错误"}


def unauthorized_response():
    return {"code": 403, "msg": "接口权限验证失败"}


def not_found_response():
    return {"code": 404, "msg": "接口不存在"}


def method_error():
    return {"code": 405, "msg": "请求方式错误"}


def not_acceptable_response():
    return {"code": 406, "msg": "请求参数不接受"}


def conflict_response():
    return {"code": 409, "msg": "冲突"}


def to_response(flag):
    if flag:
        return success_response()
    else:
        return fail_response()


def to_response_msg(flag, msg):
    if flag:
        return success_response_msg(msg)
    else:
        return fail_response_msg(msg)


def to_response_data(flag, data):
    if flag:
        return success_response_data(data)
    else:
        return fail_response_data(data)


def to_response_msg_data(flag, msg, data):
    if flag:
        return success_response_msg_data(msg, data)
    else:
        return fail_response_msg_data(msg, data)


def to_response_error_msg(flag, msg):
    if flag:
        return success_response()
    else:
        return fail_response_msg(msg)


def code_response(code):
    if code == 400:
        return param_error_response()
    elif code == 403:
        return unauthorized_response()
    elif code == 404:
        return not_found_response()
    elif code == 405:
        return method_error()
    elif code == 406:
        return not_acceptable_response()
    elif code == 409:
        return conflict_response()
    elif code == 500:
        return param_error_response()

    return fail_response()
