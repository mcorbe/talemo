"""
Settings initialization.
"""
import os

if os.environ.get("DEBUG", "False") == "True":
    from .dev import *

else:
    from .base import *
