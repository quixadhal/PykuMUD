# -*- coding: utf-8 -*- line endings: unix -*-
__author__ = 'quixadhal'

from enum import Enum
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy import orm
import log_system
from miniboa import TelnetClient
from db_system import DataBase, Session

logger = log_system.init_logging()


class LoginState(Enum):
    disconnected = 1
    connected = 2
    at_menu = 3


class Login(DataBase):
    __tablename__ = 'login'

    descriptor = Column(Integer, primary_key=True)
    remote_address = Column(String, nullable=True)
    remote_port = Column(Integer, nullable=True)
    user_id = Column(Integer, nullable=True)
    character_id = Column(Integer, nullable=True)

    def __init__(self):
        self.client = None
        self.state = LoginState.disconnected

    @orm.reconstructor
    def init_on_load(self):
        if not hasattr(self, 'client'):
            self.client = None
        if not hasattr(self, 'state'):
            self.state = LoginState.disconnected

    @classmethod
    def on_connect(cls, client: TelnetClient):
        session = Session()
        login = session.query(Login).filter(Login.descriptor == client.fileno).first()
        if not login:
            login = Login()
            login.descriptor = client.fileno
            login.client = client
            login.state = LoginState.connected
            session.add(login)
            session.commit()

    @classmethod
    def on_disconnect(cls, client: TelnetClient):
        session = Session()
        login = session.query(Login).filter(Login.descriptor == client.fileno).first()
        if login:
            # session.delete(login)
            login.state = LoginState.disconnected
            session.commit()
