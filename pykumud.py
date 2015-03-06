# -*- coding: utf-8 -*- line endings: unix -*-
__author__ = 'quixadhal'

import os
import sys
import time
import sysutils
import log_system
import serialization
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

    port = serialization.unpack(Option.get(Option.name == 'port').val)
    o2 = serialization.unpack(Option.get(Option.name == 'o2').val)
    o3 = serialization.unpack(Option.get(Option.name == 'o3').val)
    example = serialization.unpack(Option.get(Option.name == 'thing').val)
    logger.boot('Port number is %d', port)
    logger.boot('o2 string is %s', o2)
    logger.boot('o3 boolean is %s', o3)
    logger.boot('example.foo is %s', example.foo)
    if o3:
        logger.boot('o3 is true')

    time.sleep(1)
    snapshot = sysutils.ResourceSnapshot()
    logger.info(snapshot.log_data())
    logger.critical('System halted.')
