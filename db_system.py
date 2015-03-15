# -*- coding: utf-8 -*- line endings: unix -*-
__author__ = 'quixadhal'

import os
import sys
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
import log_system


logger = log_system.init_logging()
sys.path.append(os.getcwd())

Engine = create_engine('sqlite:///pykusa.db')
DataBase = declarative_base()
Session = sessionmaker(bind=Engine)


class Version(DataBase):
    __tablename__ = 'version'

    name = Column(String, primary_key=True)
    number = Column(Integer)


def init_db(to_version: int):
    connection = Engine.connect()
    if not Engine.dialect.has_table(connection, 'version'):
        from config import Option
        DataBase.metadata.create_all(Engine)
        session = Session()
        version = Version(name='database', number=to_version)
        session.add(version)
        options = Option()
        options.date_created = datetime.now()
        options.version = to_version
        options.port = 4400
        options.wizlock = False
        session.add(options)
        session.commit()
        logger.boot('Database version %d created and initialized.', version.number)

    session = Session()
    version = session.query(Version).filter(Version.name == 'database').first()
    if version.number < to_version:
        if upgrade_db(version.number, to_version):
            logger.boot('Database upgraded from version %d to version %d.', version.number, to_version)
        else:
            logger.critical('Upgrade code not provided for version %d to version %d migration!',
                            version.number, to_version)
            exit()
    else:
        logger.boot('Database version %d connected.', version.number)


def upgrade_db(from_version: int, to_version: int):
    if from_version < to_version:
        session = Session()
        version = session.query(Version).filter(Version.name == 'database').first()
        version.number = to_version
        session.add(version)
        session.commit()

    if from_version < 3:
        # Here is where we would make schema changes using the migrate() function, if needed.
        session = Session()
        # SQLite doesn't have a boolean type, an integer of values 0 or 1 is mapped instead.
        session.execute('ALTER TABLE option ADD COLUMN wizlock INTEGER DEFAULT=0')
        session.commit()

    if from_version < to_version:
        from config import Option
        session = Session()
        options = session.query(Option).first()
        options.version = to_version
        session.add(options)
        session.commit()
        return True
    return False
