# -*- coding: utf-8 -*- line endings: unix -*-
__author__ = 'quixadhal'

import os
import sys
import time
import sysutils
import log_system
import db_system


logger = log_system.init_logging()
sys.path.append(os.getcwd())

if __name__ == '__main__':
    logger.boot('System booting.')
    snapshot = sysutils.ResourceSnapshot()
    logger.info(snapshot.log_data())
    db_system.init_db()
    snapshot = sysutils.ResourceSnapshot()
    logger.info(snapshot.log_data())

    from db_system import Session
    from config import Option
    session = Session()
    options = session.query(Option).first()

    logger.boot('Using database version %s, created on %s', options.version, options.date_created)
    logger.boot('Port number is %d', options.port)
    logger.boot('Wizlock is %s', options.wizlock)

    time.sleep(1)
    snapshot = sysutils.ResourceSnapshot()
    logger.info(snapshot.log_data())
    logger.critical('System halted.')
