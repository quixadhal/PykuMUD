# -*- coding: utf-8 -*- line endings: unix -*-
__author__ = 'quixadhal'

import os
import sys
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from alembic.migration import MigrationContext
from alembic.config import Config
from alembic.script import ScriptDirectory
from alembic import command
import log_system

logger = log_system.init_logging()
sys.path.append(os.getcwd())
DB_FILE = 'pyku.db'
ALEMBIC_CONFIG = 'alembic.ini'

SQLEngine = create_engine('sqlite:///' + DB_FILE)
DataBase = declarative_base()
SessionFactory = sessionmaker(bind=SQLEngine)
Session = scoped_session(SessionFactory)


def init_db():
    connection = SQLEngine.connect()
    context = MigrationContext.configure(connection)
    current_revision = context.get_current_revision()
    logger.boot('Database revision: %s', current_revision)
    if current_revision is None:
        DataBase.metadata.create_all(SQLEngine)

    config = Config(ALEMBIC_CONFIG)
    script = ScriptDirectory.from_config(config)
    head_revision = script.get_current_head()
    if current_revision is None or current_revision != head_revision:
        logger.boot('Upgrading database to version %s.', head_revision)
        command.upgrade(config, 'head')
        from config import Option
        session = Session()
        options = session.query(Option).first()
        if options is None:
            options = Option()
        options.version = head_revision
        session.add(options)
        from pulse import Pulse
        pulse = session.query(Pulse).first()
        if pulse is None:
            pulse = Pulse()
        session.add(pulse)
        session.commit()
