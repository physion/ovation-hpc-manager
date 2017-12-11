import logging
import falcon
import jwt
import re
import os

logger = logging.getLogger('app.middleware')


def get_token(req):
    if req.auth is None:
        return None

    return re.search('^Bearer (.*)$', req.auth).group(1)


def require_auth(req, resp, resource, params):
    token = get_token(req)

    challenges = ['Bearer']

    if token is None:
        description = ('Please provide an auth token '
                       'as part of the request.')

        raise falcon.HTTPUnauthorized('Auth token required',
                                      description,
                                      challenges,
                                      href='https://api.ovation.io/')

    try:
        r = jwt.decode(token, key=os.environ['JWT_SECRET'])
        req.context["identity"] = r

    except jwt.InvalidTokenError as e:
        description = ('The provided auth token is not valid. '
                       'Please request a new token and try again.')

        raise falcon.HTTPUnauthorized('Authentication required',
                                      description,
                                      challenges,
                                      href='https://api.ovation.io/')
