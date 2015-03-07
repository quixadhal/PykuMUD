# -*- coding: utf-8 -*- line endings: unix -*-
__author__ = 'quixadhal'

import os
import sys
from datetime import datetime
# from peewee import *
from playhouse.migrate import *
import log_system


logger = log_system.init_logging()
sys.path.append(os.getcwd())
master_database = SqliteDatabase('pyku.db')
db_migrator = SqliteMigrator(master_database)


class DataBase(Model):
    class Meta:
        database = master_database


class Version(DataBase):
    name = CharField(unique=True)
    number = IntegerField()


def init_db(to_version: int):
    master_database.connect()
    if not Version.table_exists():
        from config import Option
        master_database.create_tables([Version, Option])
        version = Version.create(name='database', number=to_version)
        version.save()

        options = Option()
        options.date_created = datetime.now()
        options.port = 4400
        options.version = to_version
        options.wizlock = False
        options.save()
        logger.boot('Database version %d created and initialized.', version.number)

    version = Version.get(Version.name == 'database')
    if version.number < to_version:
        if upgrade_db(version.number, to_version):
            logger.boot('Database upgraded from version %d to version %d.', version.number, to_version)
        else:
            logger.critical('Upgrade code not provided for version %d to version %d migration!', version.number, to_version)
            exit()
    else:
        logger.boot('Database version %d connected.', version.number)


def upgrade_db(from_version: int, to_version: int):
    if from_version < to_version:
        version = Version.get(Version.name == 'database')
        version.number = to_version
        version.save()

    if from_version < 3:
        # Here is where we would make schema changes using the migrate() function, if needed.
        wizlock_field = BooleanField(default=False)
        migrate(db_migrator.add_column('option', 'wizlock', wizlock_field))

    if from_version < to_version:
        from config import Option
        options = Option.get()
        options.version = to_version
        options.save()
        return True
    return False
