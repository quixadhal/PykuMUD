# -*- coding: utf-8 -*- line endings: unix -*-
__author__ = 'quixadhal'

from enum import Enum
import log_system
from miniboa import TelnetClient

logger = log_system.init_logging()


class LoginState(Enum):
    connected = 1
    at_menu = 2


class Login(object):
    client_list = dict()

    def __init__(self, client: TelnetClient):
        if not isinstance(client, TelnetClient):
            raise TypeError('Parameter must be a TelnetClient instance!')
        self.client = client
        self.state = LoginState.connected

    @classmethod
    def on_connect(cls, client: TelnetClient):
        cls.client_list[client.fileno] = client

    @classmethod
    def on_disconnect(cls, client: TelnetClient):
        try:
            del cls.client_list[client.fileno]
        except KeyError:
            pass
