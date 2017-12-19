import logging
import sys
import os
import hpc_manager.system as system
import falcon

level = logging.DEBUG if 'DEBUG_LOG' in os.environ else logging.INFO
logging.basicConfig(stream=sys.stdout, level=level)

application = system.make_system()


if __name__ == '__main__':
    httpd = falcon.simple_server.make_server('127.0.0.1', 8000, application)
    httpd.serve_forever()
