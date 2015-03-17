# -*- coding: utf-8 -*- line endings: unix -*-
__author__ = 'quixadhal'

import os
import sys
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from alembic.migration import MigrationContext
from alembic.config import Config
from alembic.script import ScriptDirectory
from alembic import command
import log_system

logger = log_system.init_logging()
sys.path.append(os.getcwd())
DB_FILE = 'pyku.db'
ALEMBIC_CONFIG = 'alembic.ini'

Engine = create_engine('sqlite:///' + DB_FILE)
Base = declarative_base()
Session = sessionmaker(bind=Engine)


def init_db(to_version: int):
    connection = Engine.connect()
    context = MigrationContext.configure(connection)
    current_revision = context.get_current_revision()
    logger.boot('Database revision: %s', current_revision)
    if current_revision is None:
        from config import Option
        Base.metadata.create_all(Engine)
        session = Session()
        options = Option()
        options.date_created = datetime.now()
        options.version = None
        options.port = 4400
        options.wizlock = False
        session.add(options)
        session.commit()
        logger.boot('Database created and initialized.')

    config = Config(ALEMBIC_CONFIG)
    script = ScriptDirectory.from_config(config)
    head_revision = script.get_current_head()
    if current_revision is None or current_revision != head_revision:
        logger.boot('Upgrading database to version %s.', head_revision)
        command.upgrade(config, 'head')
        from config import Option
        session = Session()
        options = session.query(Option).first()
        options.version = head_revision
        session.add(options)
        session.commit()
