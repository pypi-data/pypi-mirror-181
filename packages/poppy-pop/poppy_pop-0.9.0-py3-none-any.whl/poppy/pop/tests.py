# -*- coding: utf-8 -*-
import unittest.mock as mock

import pytest
from poppy.core.test import CommandTestCase

from alembic.runtime import migration


class TestDbCommands(CommandTestCase):

    # run the test twice to verify the database rollback
    @pytest.mark.parametrize('execution_number', range(2))
    def test_load_descriptor(self, execution_number):
        from poppy.core.conf import Settings

        # define the plugin list
        plugin_list = ['poppy.pop']

        # initialize the command
        command = ['pop', 'db', 'upgrade', 'heads']

        context = migration.MigrationContext.configure(self.connection)

        # no migration should be applied yet
        assert context.get_current_revision() is None

        # force the value of the plugin list
        with mock.patch.object(Settings, 'configure',
                               autospec=True,
                               side_effect=self.mock_configure_settings(dictionary={'PLUGINS': plugin_list})):
            # run the command
            self.run_command(command)

        # check the revision hash/name
        assert context.get_current_revision() == 'poppy_pop_0001_initial'
