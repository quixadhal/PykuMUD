# -*- coding: utf-8 -*- line endings: unix -*-
__author__ = 'quixadhal'

from peewee import *
import log_system
from db_system import DataBase

logger = log_system.init_logging()


class Option(DataBase):
    date_created = DateTimeField()
    version = IntegerField()
    port = IntegerField()
    wizlock = BooleanField(default=False)
