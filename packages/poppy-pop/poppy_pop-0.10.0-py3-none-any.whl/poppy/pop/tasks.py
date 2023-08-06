#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

from sqlalchemy.orm.session import close_all_sessions
from alembic.config import Config
import alembic
from alembic import command

from poppy.core.db.dry_runner import DryRunner
from poppy.core.db.connector import Connector
from poppy.core.task import Task
from poppy.pop.plugins import Plugin
from poppy.pop.migration import MigrateError
from poppy.pop.tools import paths
from poppy.core.conf import settings
from poppy.core.logger import logger

__all__ = [
    'Execute',
    'ExecuteCli',
    'Makemigrations',
    'Upgrade',
    'Downgrade',
    'ShowCurrent',
    'CallAlembic',
    'RunAdminWebServer',
]


class DryRunTask(Task):
    def __init__(self):
        # init as usual but without related information on the database
        super().__init__()

        # force dry run
        DryRunner().activate()


@DryRunTask.as_task(plugin_name='poppy.pop', name='execute')
@Connector.if_connected(settings.MAIN_DATABASE)
def Execute(self):
    """
    To execute a script on the POPPy database.
    """
    # get the database objects for the POPPy
    database = self.pipeline.db.get_database()
    database.create_engine()

    # try closing the session to kill all current transactions
    try:
        database.scoped_session.close_all()
    except Exception as e:
        logger.error("Can't close sessions on sqlalchemy")
        logger.error(e)
        return

    # read the script
    with open(self.pipeline.properties.script, 'r') as f:
        script = f.read()

    # execute the script
    try:
        database.engine.execute(script)
    except Exception as e:
        logger.error(e)
        return


@DryRunTask.as_task(plugin_name='poppy.pop', name='execute_cli')
@Connector.if_connected(settings.MAIN_DATABASE)
def ExecuteCli(self):
    """
    To execute a script on the POPPy database from the command line.
    """
    # get the database objects for the POPPy
    database = self.pipeline.db.get_database()
    database.create_engine()

    # try closing the session to kill all current transactions
    try:
        #database.scoped_session.close_all()
        close_all_sessions()
    except Exception as e:
        logger.error("Can't close sessions on sqlalchemy")
        logger.error(e)
        return

    # execute the script if present or the command in argument
    if self.pipeline.properties.execute is None:
        script = self.pipeline.properties.input.read()
    else:
        script = self.pipeline.properties.execute
    logger.debug('Running command(s):\n{0}'.format(script))
    try:
        database.engine.execute(script)
    except Exception as e:
        logger.error(e)
        return


@DryRunTask.as_task(plugin_name='poppy.pop', name='makemigrations')
def Makemigrations(task):
    """A task to automatically generate migrations
    'alembic revision --autogenerate' is used to generate migrations.
    You have to manually edit the migration after being generated, because
    alembic cannot detect changes of table/column name etc, or does not
    generate the schema creation. More info :
    http://alembic.zzzcomputing.com/en/latest/autogenerate.html#what-does-autog
    enerate-detect-and-what-does-it-not-detect
    """
    # get the plugin to use
    plugin = task.pipeline.properties.plugin

    # check that it is valid
    if plugin not in Plugin.manager:
        raise MigrateError('{0} is not a valid registered plugin name'.format(plugin))

    database = task.pipeline.db.get_database()
    version_locations = list()
    for plugin_name in settings.PLUGINS:
        plug = Plugin.manager[plugin_name]
        location = os.path.join(plug.module.__path__[0], 'models', 'versions')
        if os.path.isdir(location):
            version_locations.append(location)

    cfg = Config()

    cfg.set_main_option('version_locations', ' '.join(version_locations))
    cfg.set_main_option('script_location', paths.from_root('alembic'))
    cfg.set_main_option('output_encoding', 'utf-8')

    database.create_engine(admin=True)
    database.create_connection()

    cfg.attributes['connection'] = database.db_connection
    cfg.attributes['plugin'] = plugin

    logger.info('Calling alembic revision')

    # used to pass arguments to alembic revision command
    # http://alembic.zzzcomputing.com/en/latest/api/commands.html#alembic.command.revision
    args = dict()
    for arg in sys.argv[4:]:
        try:
            # Only parse keyword of the form (-)-key=val
            if '=' in arg:
                s = arg.split('=')
            else:
                logger.error(
                    f'Input keyword {arg} can not be parsed and will be ignored, '
                    "please call extra alembic keywords using '='!"
                )
                continue

            # Replace any hyphen "-" by underscore "_" in keyword argument name
            # (including "-" or "--" prefix)
            s[0] = s[0].replace('-', '_')

            # Remove "_" or "__" prefix
            if s[0].startswith('__'):
                args.update({s[0][2:]: s[1]})
            elif s[0].startswith('_'):
                args.update({s[0][1:]: s[1]})
        except IndexError:
            logger.error(f'Unknown argument: {arg}, skipping!')

    command.revision(
        cfg,
        autogenerate=True,
        version_path=os.path.join(
            Plugin.manager[plugin].module.__path__[0], 'models', 'versions'
        ),
        **args,
    )

    # TODO have poppy.pop as dependency for any first migration of a plugin ?


@DryRunTask.as_task(plugin_name='poppy.pop', name='upgrade')
def Upgrade(task):
    """
    A task to do the migration of the POPPy database.
    """
    revision = task.pipeline.properties.revision

    database = task.pipeline.db.get_database()
    version_locations = list()
    for plugin_name in settings.PLUGINS:
        plug = Plugin.manager[plugin_name]
        location = os.path.join(plug.module.__path__[0], 'models', 'versions')
        if os.path.isdir(location):
            version_locations.append(location)

    cfg = Config()

    cfg.set_main_option('version_locations', ' '.join(version_locations))
    cfg.set_main_option('script_location', paths.from_root('alembic'))
    cfg.set_main_option('output_encoding', 'utf-8')

    database.create_engine(admin=True)
    database.create_connection()

    cfg.attributes['connection'] = database.db_connection
    logger.info('Calling alembic')

    command.upgrade(cfg, revision)


@DryRunTask.as_task(plugin_name='poppy.pop', name='downgrade')
def Downgrade(task):
    """
    A task to do the migration of the POPPy database.
    """
    # get the plugin to use
    revision = task.pipeline.properties.revision

    database = task.pipeline.db.get_database()
    version_locations = list()
    for plugin_name in settings.PLUGINS:
        plug = Plugin.manager[plugin_name]
        location = os.path.join(plug.module.__path__[0], 'models', 'versions')
        if os.path.isdir(location):
            version_locations.append(location)

    cfg = Config()

    cfg.set_main_option('version_locations', ' '.join(version_locations))
    cfg.set_main_option('script_location', paths.from_root('alembic'))
    cfg.set_main_option('output_encoding', 'utf-8')

    database.create_engine(admin=True)
    database.create_connection()

    cfg.attributes['connection'] = database.db_connection

    logger.info('Calling alembic')

    command.downgrade(cfg, revision)

@DryRunTask.as_task(plugin_name='poppy.pop', name='show_current')
def ShowCurrent(task):
    """
    Show the status of the current revision.
    """

    database = task.pipeline.db.get_database()
    version_locations = list()
    for plugin_name in settings.PLUGINS:
        plug = Plugin.manager[plugin_name]
        location = os.path.join(plug.module.__path__[0], 'models', 'versions')
        if os.path.isdir(location):
            version_locations.append(location)

    cfg = Config()

    cfg.set_main_option('version_locations', ' '.join(version_locations))
    cfg.set_main_option('script_location', paths.from_root('alembic'))
    cfg.set_main_option('output_encoding', 'utf-8')

    database.create_engine(admin=True)
    database.create_connection()

    cfg.attributes['connection'] = database.db_connection

    logger.info('Calling alembic')

    command.current(cfg)


@DryRunTask.as_task(plugin_name='poppy.pop', name='call_alembic')
def CallAlembic(task):
    """
    Call alembic directly
    """
    import tempfile

    TEMP_DIR = tempfile.gettempdir()

    version_locations = list()
    for plugin_name in settings.PLUGINS:
        plug = Plugin.manager[plugin_name]
        location = os.path.join(plug.module.__path__[0], 'models', 'versions')
        if os.path.isdir(location):
            version_locations.append(location)

    with open(os.path.join(TEMP_DIR, 'alembic.ini'), 'w') as f:
        f.truncate()
        f.write('[alembic]\n')
        f.write(f'script_location = {paths.from_root("alembic")}\n')
        f.write(f'version_locations = {" ".join(version_locations)}\n')
        f.write(
            f'sqlalchemy.url = {task.pipeline.db.get_database().generate_url_admin()}\n'
        )
        f.write('output_encoding = utf-8\n')

    alembicArgs = [
        '-c',
        os.path.join(TEMP_DIR, 'alembic.ini'),
        sys.argv[3],
        *sys.argv[4:],
    ]

    alembic.config.main(argv=alembicArgs)


@Task.as_task(plugin_name='poppy.pop', name='run_admin_web_server')
def RunAdminWebServer():
    from flask import Flask
    from flask_admin import Admin
    from flask_admin.contrib.sqla import ModelView
    from poppy.pop.models.job import JobLog

    # get the meb connector and get the database
    connector = Connector.manager[settings.MAIN_DATABASE]
    database = connector.get_database()

    # ensure database is connected
    database.connectDatabase()

    # get a database session
    session = database.session_factory()

    app = Flask(__name__)

    # set optional bootswatch theme
    app.config['FLASK_ADMIN_SWATCH'] = 'slate'

    # Flask and Flask-SQLAlchemy initialization here
    admin = Admin(app, name='Poppy', template_mode='bootstrap3')

    # add a model to demonstrate the usage of the admin web page
    admin.add_view(ModelView(JobLog, session))

    app.run(host='0.0.0.0')
