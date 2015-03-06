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
code_version = 2

if __name__ == '__main__':
    logger.boot('System booting.')
    snapshot = sysutils.ResourceSnapshot()
    logger.info(snapshot.log_data())
    db_system.init_db()
    snapshot = sysutils.ResourceSnapshot()
    logger.info(snapshot.log_data())

    db_version = serialization.unpack(Option.get(Option.name == 'db_version').val)
    logger.boot('Version number is %d', db_version)

    if db_version < code_version:
        logger.boot('Old database version, attempting to upgrade.')
        if db_system.upgrade_db(db_version, code_version):
            db_version = serialization.unpack(Option.get(Option.name == 'db_version').val)
            logger.boot('Success!  New version is %d', db_version)

    port = serialization.unpack(Option.get(Option.name == 'port').val)
    o2 = serialization.unpack(Option.get(Option.name == 'o2').val)
    o3 = serialization.unpack(Option.get(Option.name == 'o3').val)
    example = serialization.unpack(Option.get(Option.name == 'thing').val)
    shiny = serialization.unpack(Option.get(Option.name == 'shiny').val)
    logger.boot('Port number is %d', port)
    logger.boot('o2 string is %s', o2)
    logger.boot('o3 boolean is %s', o3)
    logger.boot('example.foo is %s', example.foo)
    logger.boot('shiny is %s', shiny)
    if o3:
        logger.boot('o3 is true')

    time.sleep(1)
    snapshot = sysutils.ResourceSnapshot()
    logger.info(snapshot.log_data())
    logger.critical('System halted.')
