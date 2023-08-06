#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from poppy.core.configuration import Configuration
from poppy.core.db.connector import Connector
from poppy.core.db.dry_runner import DryRunner
from sqlalchemy.orm.exc import MultipleResultsFound
from sqlalchemy.orm.exc import NoResultFound

__all__ = ["POPPy"]


class POPPyDatabaseError(Exception):
    """
    Errors for the connector of the POPPy database.
    """


class POPPy(Connector):
    """
    A class for querying the POPPy database.
    """

    def factory(self, database):
        """
        Return a scoped session for the descriptor to share the state of the
        database with others.
        """
        return database.scoped_session

    @property
    def configuration(self):
        return self._configuration

    @configuration.setter
    def configuration(self, configuration):
        self._configuration = configuration

        # get the descriptor file
        descriptor = Configuration.manager["descriptor"]
        self._pipeline = descriptor["pipeline.release.version"]
        self._pipeline_name = descriptor["pipeline.identifier"]
