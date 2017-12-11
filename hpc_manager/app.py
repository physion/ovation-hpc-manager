import logging
import sys
import os
import falcon
import hpc_manager.settings as settings
import hpc_manager.pubsub as pubsub
import hpc_manager.helper as helper
import hpc_manager.system as system
import hpc_manager.config as config
from hpc_manager.slurm import submit_research_job

level = logging.DEBUG if 'DEBUG_LOG' in os.environ else logging.INFO
logging.basicConfig(stream=sys.stdout, level=level)


class MakeSystem(object):
    def on_get(self, req, resp):
        req.context['result'] = {"status": "running"}
        system.make_system()
        resp.status = falcon.HTTP_200


class HpcHandler(object):
    def on_post(self, req, resp):
        body = helper.req_json(req)
        self.require_body_parameter(body, settings.ACTIVITY_ID)
        self.require_body_parameter(body, settings.USER_IMAGE)

        pubsub.make_research_callback(submit_research_job,
                                       client_id=config.secret('OVATION_CLIENT_ID'),
                                       client_secret=config.secret('OVATION_CLIENT_SECRET'),
                                       auth_domain=config.configuration('OVATION_AUTH_DOMAIN'),
                                       audience=config.configuration('OVATION_AUDIENCE'),
                                       ovation_api=config.configuration('OVATION_API_URL'),
                                       head_node=config.configuration('CLUSTER_HEAD_NODE'),
                                       key_filename=config.configuration('SSH_KEY_FILE'),
                                       host_key_file=config.configuration('KNOWN_HOSTS_FILE'),
                                       ssh_username=config.configuration('SSH_USERNAME'))

        resp.status = falcon.HTTP_201


application = falcon.API()
application.add_route('/make_system', MakeSystem())


if __name__ == '__main__':
    httpd = falcon.simple_server.make_server('127.0.0.1', 8000, application)
    httpd.serve_forever()