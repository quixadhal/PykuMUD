__author__ = 'quixadhal'
import os
import sys
import time
import log_system


sys.path.append(os.getcwd())
logger = log_system.init_logging()

import sysutils


if __name__ == '__main__':
    logger.boot('System booting.')
    snapshot = sysutils.ResourceSnapshot()
    logger.info(snapshot.log_data())
    time.sleep(1)
    snapshot = sysutils.ResourceSnapshot()
    logger.info(snapshot.log_data())
    logger.critical('System halted.')
