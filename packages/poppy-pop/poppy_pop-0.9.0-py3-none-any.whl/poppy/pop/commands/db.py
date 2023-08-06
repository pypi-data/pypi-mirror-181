#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse

from poppy.core.command import Command
from poppy.pop.tasks import ExecuteCli, CallAlembic

__all__ = []

class Db(Command):
    """
    A command to maybe allow to show status of the ROC database. But now
    essentially to allow subcommands.
    """
    __command__ = "db"
    __command_name__ = "db"
    __parent__ = "master"
    __parent_arguments__ = ["base"]
    __help__ = "Administration of the pipeline database"



class ExecuteROC(Command):
    """
    Command to execute a SQL command on the pipeline database.
    """
    __command__ = "execute"
    __command_name__ = "execute"
    __parent__ = "db"
    __parent_arguments__ = ["base"]
    __help__ = "Execute the SQL command on the ROC database"

    def add_arguments(self, parser):
        # create an exclusive group for the two options
        group = parser.add_mutually_exclusive_group(required=True)

        # add argument to set the path of the script
        group.add_argument(
            "-i",
            '--input',
            help="""
            The absolute path to the script to run on the pipeline database.
            """,
            type=argparse.FileType("r"),
            default="-",
        )

        # argument to read a command from the command line
        group.add_argument(
            "-e",
            "--execute",
            help="The command to run on the pipeline database.",
            type=str,
            default=None,
        )

    def setup_tasks(self, pipeline):
        """
        Executed to clear the database.
        """

        # the task
        task = ExecuteCli()

        # create the topology of tasks
        pipeline | task
        pipeline.start = task

class CallAlembicCommand(Command):
    """
    Commands to call alembic directly
    """
    __command__ = "alembic"
    __command_name__ = "alembic"
    __parent__ = "db"
    __parent_arguments__ = ["base"]
    __help__ = "Direct call to alembic"

    def add_arguments(self, parser):

        # argument for the command
        parser.add_argument(
            "command",
            type=str,
            help="""
            The command to give to alembic.
            """,
        )

    def setup_tasks(self, pipeline):
        """
        Show information on the current revision of the ROC database.
        """

        # the task
        task = CallAlembic()

        # create the topology of tasks
        pipeline | task
        pipeline.start = task

