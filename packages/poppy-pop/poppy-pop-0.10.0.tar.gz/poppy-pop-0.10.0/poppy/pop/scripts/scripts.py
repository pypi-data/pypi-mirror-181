#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging.config
import importlib
import os

from poppy.core.conf import settings
from poppy.core.command import Command
from poppy.core.db.handlers import load_databases
from poppy.core.configuration import Configuration
from poppy.core.tools.exceptions import print_exception
from poppy.core.plugin import Plugin
from poppy.core.generic.manager import Manager

__all__ = ['main', 'setup', 'load_config', 'load_descriptor', 'set_config', 'set_descriptor', 'pipeline_init',
           'import_module_from_path']


class LoggerNotFound(Exception):
    """
    Exception for the logger that is not found.
    """


def set_plugins_loggers_config(plugins):
    """
    Create a logger config with the correct name for each plugin in order to see what
    happens in the program in different handlers (console, console in GUI,
    activity file, etc).
    """
    # get the path from where to read the configuration file for the platform
    # set default path
    config = settings.LOGGER_CONFIG

    # loop over plugins for adding them to the logger and be fully
    # integrated with the pipeline
    for plugin in plugins:
        # add them if they are not already a module of the pipeline
        if not plugin.startswith("poppy."):
            config["loggers"][plugin] = config["loggers"]["poppy"]

    # set parameters to logging


def load_plugins(plugins):
    """
    Read the file of plugins at the fixed place and then load plugins with the
    specific work to do for the models loading, commands, etc.
    """
    # get the logger
    logger = logging.getLogger("poppy.loadPlugins")

    # get the list of plugins
    logger.debug('Load the plugin list from settings')

    # try to import the module defined
    for plugin in plugins:
        # import the module
        try:
            module = importlib.import_module(plugin)
        except Exception as e:
            print_exception(
                "Error occurred importing plugin {0}. Aborting.".format(
                    plugin,
                )
            )
            continue

        # create the plugin object
        Plugin(plugin, module)

    # now load all registered plugins
    for plugin in Plugin.manager.instances:
        try:
            plugin.load()
        except:
            print_exception(
                "Error for loading plugin {0}".format(plugin)
            )


def import_module_from_path(module_name, filepath):
    spec = importlib.util.spec_from_file_location(module_name, filepath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def setup(options):
    """
    Responsible of the setup before the generation of commands.
    """
    if options.settings:
        settings_module = import_module_from_path('settings_module', options.settings)
    elif os.environ.get('PIPELINE_SETTINGS_FILE', None):
        settings_module = import_module_from_path('settings_module', os.environ['PIPELINE_SETTINGS_FILE'])
    else:
        try:
            import settings as settings_module
        except ModuleNotFoundError:
            # search for settings in the pipeline root dir
            settings_module_path = os.path.join(settings.ROOT_DIRECTORY, 'settings.py')

            if os.path.isfile(settings_module_path):
                settings_module = import_module_from_path('settings_module', settings_module_path)
            else:
                raise Exception('No settings file found')

    # update the default settings
    settings.configure(settings_module)

    if options.log_level:
        # force the log-level of plugins
        settings.LOGGER_CONFIG['loggers']['poppy']['level'] = options.log_level

    # get the registered plugins
    plugins = settings.PLUGINS

    # set the loggers config for each non-poppy plugin
    set_plugins_loggers_config(plugins)

    # Load the logging configuration from the LOGGER_CONFIG dictionary
    logging.config.dictConfig(settings.LOGGER_CONFIG)

    # load plugins
    load_plugins(plugins)


def load_config(config_path, schema_path):
    """
    Load the data in the configuration file and set it in the class.
    """
    # read the configuration file in the XML format
    configuration = Configuration(
        config_path,
        schema_path,
        name="pipeline",
    )
    configuration.read_validate()

    # return the configuration
    return configuration


def load_descriptor(path, schema_path):
    """
    Load the data in the descriptor file and set it in the class.
    """
    # read the configuration file in the XML format
    configuration = Configuration(
        path,
        schema_path,
        name="descriptor",
    )
    configuration.read_validate()

    # return the configuration
    return configuration


def set_config(args):
    """
    Set the file name where are stored the configuration parameters.
    """
    # check environment variable
    config_path = os.getenv("PIPELINE_CONFIG_FILE", None)

    # get the path of the configuration file from the command line
    if not config_path:
        config_path = args.config

    # path for schema
    config_schema_path = args.config_schema

    # return paths
    return config_path, config_schema_path


def set_descriptor(args):
    """
    Set the file name where are stored the descriptors.
    """
    # check environment variable
    path = os.getenv("PIPELINE_DESCRIPTOR_FILE", None)

    # get the path of the configuration file from the command line
    if not path:
        path = args.descriptor

    # path for schema
    schema_path = args.pipeline_descriptor_schema

    # return paths
    return path, schema_path


def pipeline_init(args):
    """
    Used to init some things in the pipeline, without interacting with it
    directly, allowing to reuse the commands defined for the pipeline from an
    other environment where the databases, configuration, etc are already set.
    """
    # select from where to read the configuration file path
    config_path, schema_path = set_config(args)

    # load the configuration file
    args.configuration = load_config(config_path, schema_path)

    # load databases defined in the configuration
    load_databases(args.configuration["pipeline.databases"])

    # select also from where to read the descriptor of the pipeline
    descriptor_path, schema_path = set_descriptor(args)

    # load the descriptor file
    load_descriptor(descriptor_path, schema_path)

def clear_managers():
    """
    Clear the content of each instance of poppy manager.

    This operation is needed to avoid conflicts between different successive runs.

    :return:
    """

    for manager in Manager.manager_list:
        manager.delete_all()



def main(argv=None):
    """
    The main function, called when the pop program is running.
    """

    # preprocess options like --settings and --config
    # these options could affect the pipeline behavior
    # so they must be processed early.
    options, args = Command.manager.preprocess_args(argv)

    # generate possible commands
    Command.manager.generate(options)

    # parse the arguments in the command line
    Command.manager.launch(args)

    # clear pipeline managers
    clear_managers()



# connect to the signal of the command manager to set the logger before the
# generation of the commands, allowing to debug. At this place because needs to
# set also when calling directly the main function with the entry points of
# setuptools
Command.manager.generation_start.connect(setup)

# connect before the launch of the command to load databases defined in the
# configuration file, and read it also
Command.manager.run_start.connect(pipeline_init)

if __name__ == "__main__":
    main()
