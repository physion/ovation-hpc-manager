import logging
import falcon
import hpc_manager.constants as constants
import hpc_manager.helper as helper
import hpc_manager.tasks as tasks
import hpc_manager.middleware as middleware


class HpcRunResource(object):
    @falcon.before(middleware.require_auth)
    @falcon.before(middleware.max_body(64 * 1024))
    def on_post(self, req, resp):
        body = helper.req_json(req)
        logging.debug("Body:{}".format(body))

        helper.require_body_parameter(body, constants.ACTIVITY_ID)
        helper.require_body_parameter(body, constants.USER_IMAGE)
        helper.require_body_parameter(body, constants.ORGANIZATION)

        token = middleware.get_token(req)
        body[constants.TOKEN] = token

        tasks.send_message(body)

        resp.status = falcon.HTTP_CREATED


class StatusResource:
    def on_get(self, req, resp):
        """Handles GET requests"""
        quote = {
            'status': 'alive'
        }

        resp.media = quote
        resp.status = falcon.HTTP_OK


