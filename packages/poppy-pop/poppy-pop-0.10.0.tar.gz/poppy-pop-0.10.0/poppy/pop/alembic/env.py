from __future__ import with_statement

import logging
from importlib import import_module

from alembic import context
from sqlalchemy import engine_from_config, pool

logger = logging.getLogger('alembic')

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
# fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
from poppy.core.db.base import Base

target_metadata = Base.metadata


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def class_list():
    models_module = import_module(f"{config.attributes['plugin'].lower()}.models")
    models = [table_name for table_name, model_class in models_module.tables.items()]
    return models


def include_obj(obj, name, type_, reflected, compare_to):
    """Decide to include the object or not in the migration

    When a migration is generated, only the plugins models are included
    """
    if type_ == 'table':
        if name in class_list():
            return True
        else:
            return False
    else:
        return True


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True, compare_type=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        include_schemas=True,
        compare_type=True,
        include_object=include_obj
    )

    with context.begin_transaction():
        context.execute('SET search_path TO public')
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    try:
        connectable = engine_from_config(
            config.get_section(config.config_ini_section),
            prefix='sqlalchemy.',
            poolclass=pool.NullPool)
        with connectable.connect() as connection:
            run_migrations(connection)
    except KeyError:
        connection = config.attributes['connection']
        run_migrations(connection)


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
