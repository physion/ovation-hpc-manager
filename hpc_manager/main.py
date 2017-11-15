import logging
import sys
import os

import hpc_manager.system as system

if __name__ == '__main__':
    level = logging.DEBUG if 'DEBUG_LOG' in os.environ else logging.INFO
    logging.basicConfig(stream=sys.stdout, level=level)

    system.make_system()
