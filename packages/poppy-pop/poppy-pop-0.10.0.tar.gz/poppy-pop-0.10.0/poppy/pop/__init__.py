#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os

from poppy.pop import *

__all__ = ['descriptor']

_PLUGIN_DIRECTORY_PATH = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(_PLUGIN_DIRECTORY_PATH, 'descriptor.json')) as descriptor_json_file:
    # TODO: validate the json descriptor
    descriptor = json.load(descriptor_json_file)
