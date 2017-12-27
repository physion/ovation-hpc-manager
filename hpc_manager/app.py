import logging
import falcon
import hpc_manager.constants as constants
import hpc_manager.helper as helper
import hpc_manager.tasks as tasks
import hpc_manager.middleware as middleware


class HpcRunResource(object):
    #@falcon.before(middleware.require_auth)
    #@falcon.before(middleware.max_body(64 * 1024))
    def on_post(self, req, resp):
        body = req.media

        logging.info("HPC Run request: {}".format(body))

        helper.require_body_parameter(body, constants.ACTIVITY_ID)
        helper.require_body_parameter(body, constants.USER_IMAGE)
        helper.require_body_parameter(body, constants.ORGANIZATION)

        token = middleware.get_token(req)
        body[constants.TOKEN] = token

        tasks.send_message(body)

        resp.status = falcon.HTTP_CREATED
        resp.content_type = falcon.MEDIA_JSON


class StatusResource:
    def on_get(self, req, resp):
        """Handles GET requests"""

        response_body = {
            'status': 'alive'
        }

        resp.media = response_body
        resp.content_type = falcon.MEDIA_JSON
        resp.status = falcon.HTTP_OK


