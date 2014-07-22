"""
...
"""

import inspect
import os

from fabric.api import env


#
# Maximum # of releases to keep around for quick reversion.
#

env.max_releases = 5


#
# Default user created by infrastructure service e.g. AWS = ubuntu, RS = root
#

env.admin_user = 'root'


#
# User whose home directory the application structure resides.
#

env.deploy_user = 'deploy'


#
# Role Configuration
# ==================
#
# Define configuration vars needed for each role type (web, db, etc.). Keys here
# *must* match roles defined in the env.roledefs dict.
#

env.role_config = {}


#
# Role Configuration Defaults
# ===========================
#
# Defaults to merge into role configurations specified by the user, so we can
# always count on dict keys being there.
#

env.role_defaults = {
  'pgps': [],
  'sources': [],
  'ppas': [],
  'pkgs': [],
  'subtasks': { 'setup': [], 'deploy': [] }
}


#
# Application Definitions
# =======================
#
# App location and build commands, essential to building applications on the
# remote server. This dict contains a few sample applications that come with
# Texture to demonstrate capabilities and help to verify that the required
# (and desired) functionality exists.
#

env.app_config = {}


# Example Apps
# ============
#
# Apps that demonstrate the capabilities of the web server and help to verify
# that the required funtionality exists.

current_file = inspect.getfile(inspect.currentframe())
current_dir = os.path.dirname(os.path.abspath(current_file))
EXAMPLE_APPS = {
  'nodeexample':   {'local_path': current_dir + '/examples/nodeexample'},
  'phpexample':    {'local_path': current_dir + '/examples/phpexample'},
  'pythonexample': {'local_path': current_dir + '/examples/pythonexample'},
  'rackexample':   {'local_path': current_dir + '/examples/rackexample'}
}


#
# App Definition Defaults
# =======================
#
# All of the basic app def dict keys, that will be merged over by user-configured
# app defs.
#

env.app_defaults = {}


#
# Strategies
# ==========
#
# Stores configured strategies.
#

env.strategies = {}


#
# Strategy
# ========
#
# Default strategy to use when one isn't set in an app config.
#

env.strategy = 'copy'


#
# Subtasks
# ========
#
#
#

env.subtasks = {}
