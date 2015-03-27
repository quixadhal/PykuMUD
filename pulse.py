# -*- coding: utf-8 -*- line endings: unix -*-
__author__ = 'quixadhal'

"""
This module handles periodic updates of various game elements.
The actual update code might be imported from other modules, but it should
be invoked from the perform_updates() method.

Normally, only a single instance of the Pulse class should be created by the
main loop of the game, however multiple instances could be used to run multiple
game instances.  However, since the values are persisted in the database, they
would share the same speed values.
"""

from sqlalchemy import Column, Integer, Float
from sqlalchemy import orm
import time
import random
import log_system
from db_system import DataBase

logger = log_system.init_logging()


class Pulse(DataBase):
    """
    This class holds persistent timing values which control how often
    various game update systems are run, and how much time is allowed
    during each main loop iteration.
    
    Values are given as seconds, and presented as floating point numbers.
    
    Main entries are persisted in a database table.
    """
    __tablename__ = 'pulse'

    width = Column(Float, default=0.25, primary_key=True)  # 250ms per "tick"
    violence = Column(Float, default=1.5)  # combat rounds
    river = Column(Float, default=2.5)  # river current movement
    teleport = Column(Float, default=2.5)  # teleport movement
    nature = Column(Float, default=5.0)  # poison/hunger/etc
    mobile = Column(Float, default=6.0)  # npc wandering
    sound = Column(Float, default=8.0)  # zone chatter
    zone = Column(Float, default=60.0)  # zone updates
    update = Column(Float, default=70.0)  # weather, spell effects, healing
    variation = Column(Float, default=7.5)  # variability in update

    def __init__(self):
        self._point = dict()

    @orm.reconstructor
    def init_on_load(self):
        now = time.time()
        self._point = dict()
        self._point['violence'] = now + self.violence
        self._point['river'] = now + self.river
        self._point['teleport'] = now + self.teleport
        self._point['nature'] = now + self.nature
        self._point['mobile'] = now + self.mobile
        self._point['sound'] = now + self.sound
        self._point['zone'] = now + self.zone
        self._point['update'] = now + self.update
        logger.debug('now == %s (%f)', time.ctime(now), now)
        logger.debug('tick len == %f', self.violence)
        logger.debug('tick time == %s (%f)', time.ctime(self._point['violence']), self._point['violence'])

    def perform_updates(self):
        now = time.time()
        if now >= self._point['violence']:
            logger.debug('Doing violence')
            self._point['violence'] = time.time() + self.violence
        if now >= self._point['river']:
            logger.debug('Doing river')
            self._point['river'] = time.time() + self.river
        if now >= self._point['teleport']:
            logger.debug('Doing teleport')
            self._point['teleport'] = time.time() + self.teleport
        if now >= self._point['nature']:
            logger.debug('Doing nature')
            self._point['nature'] = time.time() + self.nature
        if now >= self._point['mobile']:
            logger.debug('Doing mobile')
            self._point['mobile'] = time.time() + self.mobile
        if now >= self._point['sound']:
            logger.debug('Doing sound')
            self._point['sound'] = time.time() + self.sound
        if now >= self._point['zone']:
            logger.debug('Doing zone')
            self._point['zone'] = time.time() + self.zone
        if now >= self._point['update']:
            logger.debug('Doing update')
            self._point['update'] = time.time() + self.update + random.uniform(-self.variation, self.variation)
