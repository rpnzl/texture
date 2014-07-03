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
  'tasks': []
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

current_file = inspect.getfile(inspect.currentframe())
current_dir = os.path.dirname(os.path.abspath(current_file))

env.apps = {

  # Example Apps
  # ============
  #
  # Apps that demonstrate the capabilities of the web server and help to verify
  # that the required funtionality exists.

  'nodeexample': {
    'local_path': current_dir + '/examples/nodeexample',
    'max_releases': 1
  },
  'phpexample': {
    'local_path': current_dir + '/examples/phpexample',
    'max_releases': 1
  },
  'pythonexample': {
    'local_path': current_dir + '/examples/pythonexample',
    'max_releases': 1
  },
  'rackexample': {
    'local_path': current_dir + '/examples/rackexample',
    'max_releases': 1
  }
}


#
# App Definition Defaults
# =======================
#
# All of the basic app def dict keys, that will be merged over by user-configured
# app defs.
#

APP_DEFAULTS = {
  'local_path': None,
  'shared_dirs': [],
  'max_releases': None,
  'strategy': 'git',
  'branch': 'master'
}


#
# Strategies
# ==========
#
# Stores configured strategies.
#

env.strategies = {}
