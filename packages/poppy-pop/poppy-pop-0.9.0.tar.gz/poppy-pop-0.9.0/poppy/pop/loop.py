#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from poppy.core.loop import LegacyLoop
from poppy.core.logger import logger

class Loop(LegacyLoop):
    def __init__(self, *args, **kwargs):
        logger.warning("Deprecation Warning: you should use the new 'Loop' class located in 'poppy.core.loop'")
        super().__init__(*args, **kwargs)