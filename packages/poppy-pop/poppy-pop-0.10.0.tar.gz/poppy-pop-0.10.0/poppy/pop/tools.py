#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os.path as osp
import hashlib

from poppy.core.generic.paths import Paths

__all__ = ["paths", "compute_file_sha"]

_ROOT_DIRECTORY = osp.abspath(
    osp.dirname(__file__)
)

paths = Paths(_ROOT_DIRECTORY)


def compute_file_sha(file,
                     buf_size=65536):
    """Compute SHA256 of an input file."""
    sha = hashlib.sha256()
    with open(file, 'rb') as f:
        while True:
            data = f.read(buf_size)
            if not data:
                break
            sha.update(data)

    return sha
