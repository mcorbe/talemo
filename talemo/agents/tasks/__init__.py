"""
Import tasks from the agents app.

This module imports the task functions directly from the tasks.py file
using importlib to avoid circular imports.
"""
import sys
import os
import importlib.util

# Directly load the tasks.py module without going through the package
module_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "tasks.py")
spec = importlib.util.spec_from_file_location("tasks_module", module_path)
tasks_module = importlib.util.module_from_spec(spec)
sys.modules["tasks_module"] = tasks_module
spec.loader.exec_module(tasks_module)

# Re-export the task functions to maintain the expected API
generate_story = tasks_module.generate_story
enhance_story = tasks_module.enhance_story

__all__ = ['generate_story', 'enhance_story']
