from django.http import JsonResponse, HttpResponse


class HttpCode(object):
    ok = 200
    paramserror = 400
    unauth = 401
    methoderror = 405
    servererror = 500


def result(code=HttpCode.ok, message="", data=None, kwargs=None):
    json_dict = {"code": code, "message": message, "data": data}

    if kwargs and isinstance(kwargs, dict) and kwargs.keys():
        json_dict.update(kwargs)
    return JsonResponse(json_dict)
    # return HttpResponse(json.dumps(json_dict, cls=DjangoJSONEncoder), content_type="application/json")


def ok(message=""):
    return result(message=message)


def params_error(message="", data=None):
    return result(code=HttpCode.paramserror, message=message)


def unauth(message="", data=None):
    return result(code=HttpCode.unauth, message=message)


def method_error(message="", data=None):
    return result(code=HttpCode.methoderror, message=message)


def server_error(message="", data=None):
    return result(code=HttpCode.servererror, message=message)



