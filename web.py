# -*- coding: utf-8 -*- line endings: unix -*-
__author__ = 'quixadhal'

import os
import cherrypy
import log_system

logger = log_system.init_logging()


def start_web_server():
    # server_config = os.path.join()
    server = WebServer()
    # cherrypy.config.update(server_config)
    cherrypy.tree.mount(server, "")  # , config=server_config)
    cherrypy.engine.start()
    logger.boot('Web server started')


class WebServer(object):
    @cherrypy.expose
    def index(self):
        return "Testing"

