# -*- coding: utf-8 -*- line endings: unix -*-
__author__ = 'quixadhal'

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
import log_system
from db_system import DataBase

logger = log_system.init_logging()


class Option(DataBase):
    __tablename__ = 'option'

    date_created = Column(DateTime, primary_key=True, default=datetime.now)
    version = Column(String)
    port = Column(Integer, default=4400)
    wizlock = Column(Boolean, default=False)
    hotboot = Column(Boolean, default=False)
