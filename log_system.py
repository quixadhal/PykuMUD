# -*- coding: utf-8 -*- line endings: unix -*-
__author__ = 'quixadhal'

import logging

# Define a few custom log levels
# WileyMUD had INFO, ERROR, FATAL, BOOT, AUTH, KILL, DEATH, RESET, and IMC
# Default Python logging levels are CRITICAL 50, ERROR 40, WARNING 30, INFO 20, DEBUG 10


master_logger = None


def auth_log(self, message, *args, **kws):
    if self.level <= 39:
        self._log(39, message, args, **kws)


def player_kill_log(self, message, *args, **kws):
    if self.level <= 38:
        self._log(38, message, args, **kws)


def boot_log(self, message, *args, **kws):
    if self.level <= 31:
        self._log(31, message, args, **kws)


def reset_log(self, message, *args, **kws):
    if self.level <= 29:
        self._log(29, message, args, **kws)


def kill_log(self, message, *args, **kws):
    if self.level <= 21:
        self._log(21, message, args, **kws)


def init_logging():
    global master_logger

    if master_logger is None:
        logging.basicConfig(format='%(asctime)s %(levelname)-8s %(module)16s| %(message)s', level=logging.DEBUG)
        logging.addLevelName(39, 'AUTH')
        logging.addLevelName(38, 'PLAYER_KILL')
        logging.addLevelName(31, 'BOOT')
        logging.addLevelName(29, 'RESET')
        logging.addLevelName(21, 'KILL')
        logging.Logger.auth = auth_log
        logging.Logger.player_kill = player_kill_log
        logging.Logger.boot = boot_log
        logging.Logger.reset = reset_log
        logging.Logger.kill = kill_log
        master_logger = logging.getLogger()
    return master_logger
