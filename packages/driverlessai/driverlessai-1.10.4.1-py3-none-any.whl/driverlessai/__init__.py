#!/usr/bin/env python
# Copyright 2020 H2O.ai; Proprietary License;  -*- encoding: utf-8 -*-

import sys

from driverlessai import token_providers
from driverlessai.__about__ import __build_info__, __version__
from driverlessai._core import Client, is_server_up

__all__ = [
    "__version__",
    "__build_info__",
    "Client",
    "is_server_up",
    "token_providers",
]

if sys.version_info[0] == 3 and sys.version_info[1] <= 6:
    print("Warning! Support for Python 3.6 will be dropped from v1.10.5 onwards.")
