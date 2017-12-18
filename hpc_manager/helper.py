import json
import falcon


def req_json(req):
    """
    Gets the JSON body from req (already processed by JSONTranslator)
    """
    _req_json = req.stream.read().decode('utf8').replace("'", '"')
    return json.loads(_req_json)


def require_body_parameter(body, key):
    if key not in body:
        raise falcon.HTTPBadRequest("Bad Request", "{} id required".format(key))