import StringIO, os
from fabric.api import run, env, task, parallel, puts, execute
from fabric.contrib import files
from fabric.colors import red, yellow
from cuisine import *

#
# Maximum # of releases to keep around for reversion.
#

env.max_releases = 5

#
# Default user created by infrastructure service e.g. AWS = ubuntu, RS = root
#

env.administrative_user = 'root'

#
# User whose home directory the application structure resides.
#

env.deployment_user = 'deploy'

#
# Role Configuration
# ==================
#
# Define configuration vars needed for each role type (web, db, etc.). Keys here
# *must* match roles defined in the env.roledefs dict.
#

env.roleconfig = {}

#
# Role Configuration Defaults
# ===========================
#
# Defaults to merge into role configurations specified by the user, so we can
# always count on dict keys being there.
#

ROLE_DEFAULTS = { 'pgps': [], 'sources': [], 'ppas': [], 'pkgs': [] }

#
# Application Definitions
# =======================
#
# App location and build commands, essential to building applications on the
# remote server.
#

env.apps = {}

#
# App Definition Defaults
# =======================
#
# All of the basic app def dict keys, that will be merged over by user-configured
# app defs.
#

APP_DEFAULTS = { 'local_path': None, 'shared_dirs': [] }

#
# Example Applications
# ====================
#
# Apps that demonstrate the capabilities of the web server and help to verify
# that the required funtionality exists.
#

EXAMPLE_APPS = {
  'nodeexample': {
    'local_path': 'resources/examples/nodeexample'
  },
  'phpexample': {
    'local_path': 'resources/examples/phpexample'
  },
  'pythonexample': {
    'local_path': 'resources/examples/pythonexample'
  },
  'rackexample': {
    'local_path': 'resources/examples/rackexample'
  }
}

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# HELPER FUNCS ----------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

#
#
#

@task
def install_pgps(items):
  """ ... """
  print(yellow("Installing PGPs."))
  for pgp in items:
    run(" ".join([
      "apt-key adv --keyserver",
      pgp['server'],
      "--recv-keys",
      pgp['key']
    ]))

#
#
#

@task
def install_sources(items):
  """ ... """
  print(yellow("Adding sources."))
  for source in items:
    file_ensure(source['path'], owner='root')
    for line in source['lines']:
      files.append(source['path'], line, use_sudo=True)

#
#
#

@task
def install_ppas(items):
  """ ... """
  print(yellow("Adding PPAs."))
  for ppa in items:
    repository_ensure_apt(ppa)

#
#
#

@task
def install_pkgs(items):
  """ ... """
  print(yellow("Installing packages."))
  package_update()
  package_upgrade()
  package_ensure(' '.join(items))

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# TASKS -----------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

@task
@parallel(pool_size=5)
def setup(role):
  """ ... """
  if role not in env.roledefs or role not in env.roleconfig:
    print(red("Please specify a valid role for setup."))
  else:
    role_config = ROLE_DEFAULTS.copy()
    role_config.update(env.roleconfig[role])

    env.hosts = env.roledefs[role]
    env.user  = env.administrative_user

    with mode_sudo():
      # execute('install_pgps',    role_config['pgps'])
      # execute('install_sources', role_config['sources'])
      # execute('install_ppas',    role_config['ppas'])
      # execute('install_pkgs',    role_config['pkgs'])

      for setup_task in role_config['setup_tasks']:
        execute(setup_task)
