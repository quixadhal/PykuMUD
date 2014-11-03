# -*- coding: utf-8 -*- line endings: unix -*-
__author__ = 'quixadhal'

import os
import sys
import log_system
from peewee import *


logger = log_system.init_logging()
sys.path.append(os.getcwd())
master_database = SqliteDatabase('pyku.db')


class DataBase(Model):
    class Meta:
        database = master_database


class Option(DataBase):
    name = CharField(unique=True)
    val = CharField()


def init_db():
    master_database.connect()
    if not Option.table_exists():
        master_database.create_tables([Option], True)
        port = Option.create(name='port', val='4400')
        port.save()
        logger.boot('Database initialized.')
