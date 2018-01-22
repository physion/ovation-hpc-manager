import json
import falcon

def require_body_parameter(body, key):
    if key not in body:
        raise falcon.HTTPBadRequest("Bad Request", "{} id required".format(key))
