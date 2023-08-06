#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from poppy.core.logger import logger
from poppy.core.plugin import Plugin as CorePlugin, PluginError as CorePluginError


__all__ = ["Plugin"]


# ensure backward compatibility
class PluginError(CorePluginError):
    def __init__(self, *args, **kwargs):
        logger.warning("Deprecation Warning: the 'PluginError' class was moved in 'poppy.core.plugin'")
        super().__init__(*args, **kwargs)

class Plugin(CorePlugin):
    def __init__(self, *args, **kwargs):
        logger.warning("Deprecation Warning: the 'Plugin' class was moved in 'poppy.core.plugin'")
        super().__init__(*args, **kwargs)