"""Top-level package for Coding Dojo Data Science."""

__author__ = """James Irving"""
__email__ = 'james.irving.phd@gmail.com'
__version__ = '1.1.0'

from . import datasets
# from .inspect import check_package_versions
# from cdds import lp_functions as lp
from . import lp_functions
from . import inspect
from . import utils

from .inspect import ihelp 
from .cdds import dojo_env_setup_instructions