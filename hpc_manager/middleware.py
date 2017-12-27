import logging
import falcon
import jwt
import re
import os

logger = logging.getLogger('middleware')


class RequestLoggerMiddleware(object):
    def process_resource(self, req, resp, resource, params):
        logger.info('{} {} {} {}'.format(req.forwarded_scheme,
                                         req.forwarded_host,
                                         req.method,
                                         req.relative_uri))

    def process_response(self, req, resp, resource, req_succeeded):
        logger.info('{} {} {} {} {}'.format(req.forwarded_scheme,
                                            req.forwarded_host,
                                            req.method,
                                            req.relative_uri,
                                            resp.status))

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


def max_body(limit):
    def hook(req, resp, resource, params):
        length = req.content_length
        if length is not None and length > limit:
            msg = ('The size of the request is too large. The body must not '
                   'exceed ' + str(limit) + ' bytes in length.')

            raise falcon.HTTPRequestEntityTooLarge(
                'Request body is too large', msg)

    return hook
