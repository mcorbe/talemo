"""
Settings initialization.
"""
import os
import logging

# Fix the DEBUG environment variable parsing
debug_setting = os.environ.get("DEBUG", "False").lower() == "true"

if debug_setting:
    logging.info("Loading development settings")
    from .dev import *
else:
    logging.info("Loading settings")
    from .base import *