import logging
import sys
import os
import falcon
import hpc_manager.settings as settings
import hpc_manager.pubsub as pubsub
import hpc_manager.helper as helper
import hpc_manager.system as system
import hpc_manager.middleware as middleware

level = logging.DEBUG if 'DEBUG_LOG' in os.environ else logging.INFO
logging.basicConfig(stream=sys.stdout, level=level)


class MakeSystem(object):
    def on_get(self, req, resp):
        req.context['result'] = {"status": "running"}
        logging.info("Testing make system")
        system.make_system()
        resp.status = falcon.HTTP_200


class HpcHandler(object):
    @falcon.before(middleware.require_auth)
    @falcon.before(middleware.max_body(64 * 1024))
    def on_post(self, req, resp):
        logging.info("Testing post")
        body = helper.req_json(req)
        logging.info("Body:{}".format(body))

        helper.require_body_parameter(body, settings.ACTIVITY_ID)
        helper.require_body_parameter(body, settings.USER_IMAGE)
        helper.require_body_parameter(body, settings.ORGANIZATION)

        token = middleware.get_token(req)
        body["token"] = token

        system.send_message(body)

        resp.status = falcon.HTTP_201


application = falcon.API()
#application.add_route('/make_system', MakeSystem())
application.add_route('/hpc_run', HpcHandler())

if __name__ == '__main__':
    httpd = falcon.simple_server.make_server('127.0.0.1', 8000, application)
    httpd.serve_forever()