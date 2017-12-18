import logging
import sys
import os
import hpc_manager.app as app
import hpc_manager.system as system
import falcon


application = system.make_system()
application.add_route('/hpc_run', app.HpcHandler())


if __name__ == '__main__':
    level = logging.DEBUG if 'DEBUG_LOG' in os.environ else logging.INFO
    logging.basicConfig(stream=sys.stdout, level=level)
    httpd = falcon.simple_server.make_server('127.0.0.1', 8000, application)
    httpd.serve_forever()