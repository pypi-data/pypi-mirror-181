#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from poppy.core.command import Command
from poppy.pop.tasks import Downgrade
from poppy.pop.tasks import Upgrade
#from poppy.pop.tasks import set_current
from poppy.pop.tasks import ShowCurrent
from poppy.pop.tasks import Makemigrations

__all__ = []


class MigratorUpgradeCommand(Command):
    """
    Commands relative to the migrator for the pipeline database.
    """
    __command__ = 'migrator_upgrade'
    __command_name__ = 'upgrade'
    __parent__ = 'db'
    __parent_arguments__ = ['base']
    __help__ = 'Upgrade the pipeline database to the specified revision'

    def add_arguments(self, parser):
        """
        Add arguments for the migration of the database for a given plugin and
        to a given revision.
        """

        # and an argument for the revision to move on
        parser.add_argument(
            'revision',
            type=str,
            default=None,
            nargs='?',
            help="""
            The revision of the database to switch on. Can be either 'head' for
            the last revision, or an unique identifier of the revision (for
            example 'ae1' for the revision 'ae1027a6acf'), or a decimal value
            '+N' N being the number of revisions to execute from the current one.
            """
        )

    def setup_tasks(self, pipeline):
        """
        Executed to update the database.
        """

        # the task
        task = Upgrade()

        # create the topology of tasks
        pipeline | task
        pipeline.start = task


class MigratorDowngradeCommand(Command):
    """
    Commands relative to the migrator for the poppy database.
    """
    __command__ = 'migrator_downgrade'
    __command_name__ = 'downgrade'
    __parent__ = 'db'
    __parent_arguments__ = ['base']
    __help__ = 'Downgrade the POPPy database to the specified revision'

    def add_arguments(self, parser):
        """
        Add arguments for the migration of the database for a given plugin and
        to a given revision.
        """

        # and an argument for the revision to move on
        parser.add_argument(
            'revision',
            type=str,
            default=None,
            nargs='?',
            help="""
            The revision of the database to switch on. Can be a unique
            identifier of the revision (for example 'ae1' for the revision
            'ae1027a6acf'), or a decimal value '-N' N being the number of
            revisions to downgrade from the current one.
            one.
        """
        )

    def setup_tasks(self, pipeline):
        """
        Executed to downgrade the database.
        """

        # the task
        task = Downgrade()

        # create the topology of tasks
        pipeline | task
        pipeline.start = task


class MigratorCurrentCommand(Command):
    """
    Commands relative to the migrator for the poppy database.
    """
    __command__ = 'migrator_current'
    __command_name__ = 'current'
    __parent__ = 'db'
    __parent_arguments__ = ['base']
    __help__ = 'Show information on the current revision of the POPPy database'

    def setup_tasks(self, pipeline):
        """
        Show information on the current revision of the POPPy database.
        """

        # the task
        task = ShowCurrent()

        # create the topology of tasks
        pipeline | task
        pipeline.start = task


class MigratorMakemigrationsCommand(Command):
    """
    Commands to call the generation of migrations
    """
    __command__ = 'migrator_makemigrations'
    __command_name__ = 'makemigrations'
    __parent__ = 'db'
    __parent_arguments__ = ['base']
    __help__ = 'Show information on the current revision of the POPPy database'

    def add_arguments(self, parser):
        """
        Add arguments for the migration of the database for a given plugin
        """
        # argument for the plugin to use
        parser.add_argument(
            'plugin',
            type=str,
            help="""
            The name of the plugin for which the migration will be applied.
            """,
        )

    def setup_tasks(self, pipeline):
        """
        Show information on the current revision of the POPPy database.
        """

        # the task
        task = Makemigrations()

        # create the topology of tasks
        pipeline | task
        pipeline.start = task

# TODO - Make this command functional (not set_current() method in poppy.pop.tasks)
# class MigratorSetCurrentCommand(Command):
#     """
#     Commands relative to the migrator for the poppy database.
#     """
#     __command__ = "migrator_current_set"
#     __command_name__ = "set"
#     __parent__ = "migrator_current"
#     __parent_arguments__ = ["base"]
#     __help__ = "Set the current revision for the plugin in argument"
#
#     def add_arguments(self, parser):
#         """
#         Add arguments for the migration of the database for a given plugin and
#         to a given revision.
#         """
#         # argument for the plugin to use
#         parser.add_argument(
#             "plugin",
#             type=str,
#             help="""
#             The name of the plugin to use to know the current revision. If not
#             provided, information for all plugins in the migrator schema are
#             shown.
#             """,
#         )
#
#         # argument for the revision to set
#         parser.add_argument(
#             "revision",
#             type=str,
#             nargs="?",
#             default=None,
#             help="""
#             The revision of the plugin to set on the migrator database. if not
#             provided, it will be None, i.e. the first state of the database
#             before any migration applied.
#             """,
#         )
#
#     def __call__(self, args):
#         """
#         Executed to downgrade the database.
#         """
#         # create the pipeline
#         pipeline = Pop(args)
#
#         # the task
#         task = set_current()
#
#         # create the topology of tasks
#         pipeline | task
#         pipeline.start = task
#
#         # run the pipeline
#         pipeline.run()
