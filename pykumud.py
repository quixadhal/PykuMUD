__author__ = 'quixadhal'
import os, sys
import time
import logging


def boot_log(self, message, *args, **kws):
    self._log(21, message, args, **kws)

sys.path.append(os.getcwd())
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(module)16s| %(message)s', level=logging.DEBUG)
logging.addLevelName(21, 'BOOT')
logging.Logger.boot = boot_log
logger = logging.getLogger()

import sysutils


if __name__ == '__main__':
    logger.boot('System booting.')
    snapshot = sysutils.ResourceSnapshot()
    logger.info(snapshot.log_data())
    time.sleep(1)
    snapshot = sysutils.ResourceSnapshot()
    logger.info(snapshot.log_data())
    logger.critical('System halted.')
