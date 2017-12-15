import logging
import sys
import os
import falcon
import hpc_manager.settings as settings
import hpc_manager.helper as helper
import hpc_manager.controller as controller
import hpc_manager.middleware as middleware


class HpcHandler(object):
    @falcon.before(middleware.require_auth)
    @falcon.before(middleware.max_body(64 * 1024))
    def on_post(self, req, resp):
        body = helper.req_json(req)
        logging.debug("Body:{}".format(body))

        helper.require_body_parameter(body, settings.ACTIVITY_ID)
        helper.require_body_parameter(body, settings.USER_IMAGE)
        helper.require_body_parameter(body, settings.ORGANIZATION)

        token = middleware.get_token(req)
        body[settings.TOKEN] = token

        controller.send_message(body)

        resp.status = falcon.HTTP_201


application = falcon.API()
application.add_route('/hpc_run', HpcHandler())


if __name__ == '__main__':
    level = logging.DEBUG if 'DEBUG_LOG' in os.environ else logging.INFO
    logging.basicConfig(stream=sys.stdout, level=level)

    httpd = falcon.simple_server.make_server('127.0.0.1', 8000, application)
    httpd.serve_forever()