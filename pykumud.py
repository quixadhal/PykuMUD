__author__ = 'quixadhal'
import os
import sys
import time
import sysutils
import log_system
import db_system
from db_system import Option


logger = log_system.init_logging()
sys.path.append(os.getcwd())


if __name__ == '__main__':
    logger.boot('System booting.')
    snapshot = sysutils.ResourceSnapshot()
    logger.info(snapshot.log_data())
    db_system.init_db()
    snapshot = sysutils.ResourceSnapshot()
    logger.info(snapshot.log_data())
    port = int(Option.get(Option.name == 'port').val)
    logger.boot('Port number is %d', port)
    time.sleep(1)
    snapshot = sysutils.ResourceSnapshot()
    logger.info(snapshot.log_data())
    logger.critical('System halted.')
