# -*- coding: utf-8 -*- line endings: unix -*-
__author__ = 'quixadhal'

import os
import sys
from peewee import *
import log_system
import serialization


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
        port = Option.create(name='port', val=serialization.pack(4400))
        o2 = Option.create(name='o2', val=serialization.pack('stuff'))
        o3 = Option.create(name='o3', val=serialization.pack(False))
        port.save()
        o2.save()
        o3.save()
        logger.boot('Database initialized.')
