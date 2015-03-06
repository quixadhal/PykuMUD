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
        db_version = Option.create(name='db_version', val=serialization.pack(1))
        port = Option.create(name='port', val=serialization.pack(4400))
        o2 = Option.create(name='o2', val=serialization.pack('stuff'))
        o3 = Option.create(name='o3', val=serialization.pack(False))
        example = serialization.ExampleThing()
        thing = Option.create(name='thing', val=serialization.pack(example))
        db_version.save()
        port.save()
        o2.save()
        o3.save()
        thing.save()
        logger.boot('Database initialized.')


def upgrade_db(from_version: int, to_version: int):
    if from_version == 1:
        shiny = Option.create(name='shiny', val=serialization.pack('all your base are belong to us'))
        shiny.save()
        db_version_obj = Option.get(Option.name == 'db_version')
        db_version_obj.val = serialization.pack(to_version)
        db_version_obj.save()
        return True
    return False
