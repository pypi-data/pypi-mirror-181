#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest

from poppy.core.command import Command
from poppy.core.conf import settings
from poppy.core.logger import logger

__all__ = []


class Test(Command):
    """
    A command to run pytest to discover and run tests.
    """
    __command__ = 'test'
    __command_name__ = 'test'
    __parent__ = 'master'
    __parent_arguments__ = ['base']
    __help__ = 'Runs pytest to discover and run tests'

    def add_arguments(self, parser):
        # by default, test all the registered plugins
        parser.add_argument(
            '--plugin-list',
            help="""
            List of plugins to be tested.
            """,
            nargs='+',
            default=['poppy.core', ] + settings.PLUGINS
        )

        parser.add_argument(
            '--junit-xml',
            help='Create JUnitXML reports'
        )
        parser.add_argument(
            '--cov-report',
            help="Type and path of generated report(s) (multi-allowed). Examples: 'html:/path/to/html/dir', 'xml:/path/to/xml/file.xml'.",
            nargs='+',
            action='append'
        )

        parser.add_argument(
            '-s',
            '--no-capture',
            help='Per-test capturing method: no',
            action='store_true'
        )

        parser.add_argument(
            "--pudb",
            help='Calls interactive debugger (needs to have the pytest-pudb package)',
            action='store_true'
        )
        parser.add_argument(
            "--tb",
            help="Traceback options",
            action='append'
        )
        parser.add_argument(
            "-r",
            "--report",
            help="Summary report options",
            action='append'
        )
        parser.add_argument(
            "-v",
            "--verbose",
            help="increase verbosity",
            action='store_true'
        )

        parser.add_argument(
            "--timeout",
            help="The test will fail if the execution time is grater than <timeout>",
            type=int,
            default=300
        )



    def setup_tasks(self, pipeline):
        """
        Executed to run pytest on each listed plugin.
        """
        logger.info(f'Testing the following plugins: {pipeline.args.plugin_list}')

        # list all the test modules
        plugin_test_module_list = list(map(lambda x: x + '.tests', pipeline.args.plugin_list))

        pytest_args = ['--pyargs', ] + plugin_test_module_list

        if pipeline.args.junit_xml:
            pytest_args = ['--junitxml', pipeline.args.junit_xml] + pytest_args

        if pipeline.args.cov_report:
            for plugin in pipeline.args.plugin_list:
                pytest_args += ['--cov', plugin]
            for cov_arg_list in pipeline.args.cov_report:
                for cov_arg in cov_arg_list:
                    pytest_args += ['--cov-report', cov_arg]

        if pipeline.args.no_capture:
            pytest_args += ['-s']

        if pipeline.args.pudb:
            pytest_args += ['--pudb']

        if pipeline.args.tb:
            pytest_args += ['--tb={}'.format(pipeline.args.tb[0])]

        if pipeline.args.report:
            pytest_args += ['-r{}'.format(pipeline.args.report[0])]

        if pipeline.args.verbose:
            pytest_args += ['-vv']

        if pipeline.args.timeout:
            pytest_args += ['--timeout={}'.format(pipeline.args.timeout)]

        # Indicate that there is no entry point for the pipeline
        # (To avoid error message)
        pipeline.no_entry_point = True

        # run pytest on each module
        pytest.main(pytest_args)
