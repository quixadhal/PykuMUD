# -*- coding: utf-8 -*- line endings: unix -*-
__author__ = 'quixadhal'

import os
import sys
import time
import sysutils
import log_system
import db_system
from config import Option


logger = log_system.init_logging()
sys.path.append(os.getcwd())
code_version = 2

if __name__ == '__main__':
    logger.boot('System booting.')
    snapshot = sysutils.ResourceSnapshot()
    logger.info(snapshot.log_data())
    db_system.init_db(code_version)
    snapshot = sysutils.ResourceSnapshot()
    logger.info(snapshot.log_data())

    options = Option.get()

    logger.boot('Using database version %d, created on %s', options.version, options.date_created)
    logger.boot('Port number is %d', options.port)

    time.sleep(1)
    snapshot = sysutils.ResourceSnapshot()
    logger.info(snapshot.log_data())
    logger.critical('System halted.')
