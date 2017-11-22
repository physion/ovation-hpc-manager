import logging
import sys
import os

import hpc_manager.system as system

level = logging.DEBUG if 'DEBUG_LOG' in os.environ else logging.INFO
logging.basicConfig(stream=sys.stdout, level=level)

application = system.make_system()