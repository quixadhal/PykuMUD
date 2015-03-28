# -*- coding: utf-8 -*- line endings: unix -*-
__author__ = 'quixadhal'

import os
import sys
import time
import sysutils
import log_system
import db_system
import miniboa


logger = log_system.init_logging()
sys.path.append(os.getcwd())


def PykuMUD():
    logger.boot('System booting.')
    start_snapshot = sysutils.ResourceSnapshot()
    logger.boot(start_snapshot.log_data())
    db_system.init_db()
    from db_system import Session
    from config import Option
    session = Session()
    options = session.query(Option).first()
    logger.boot('Using database version %s, created on %s', options.version, options.date_created)
    from pulse import Pulse
    pulse = session.query(Pulse).first()
    server = miniboa.TelnetServer(port=options.port, timeout=0.0)
    logger.boot('PykuMUD ready on port %d', options.port)
    done = False
    while not done:
        top_of_loop = time.time()
        server.poll()
        # process input
        pulse.perform_updates()
        time_spent = time.time() - top_of_loop
        nap_time = pulse.width - time_spent
        if nap_time > 0.0:
            time.sleep(nap_time)
        else:
            logger.warn('Exceeded time slice by %.3f seconds!', abs(nap_time))

    logger.critical('System halted.')

if __name__ == '__main__':
    PykuMUD()
