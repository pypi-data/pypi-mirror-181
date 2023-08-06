#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from poppy.core.command import Command
from poppy.pop.tasks import RunAdminWebServer

__all__ = []


class WebAdmin(Command):
    """
    A command to launch a local web server to manage the pipeline database
    """
    __command__ = "web_admin"
    __command_name__ = "web_admin"
    __parent__ = "master"
    __parent_arguments__ = ["base"]
    __help__ = "Administration of the pipeline database via a web server"

    def setup_tasks(self, pipeline):
        run_admin_web_server = RunAdminWebServer()

        pipeline | run_admin_web_server
        pipeline.start = run_admin_web_server
