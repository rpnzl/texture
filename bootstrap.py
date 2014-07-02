import inspect, StringIO, os, sys
from fabric.api import run, env, task, parallel, puts, execute, put
from fabric.contrib import files
from fabric.colors import red, yellow
from cuisine import *
from strategy import *

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

APP_DEFAULTS = {
  'local_path': None,
  'shared_dirs': [],
  'max_releases': None,
  'strategy': 'git',
  'branch': 'master'
}

#
# Example Applications
# ====================
#
# Apps that demonstrate the capabilities of the web server and help to verify
# that the required funtionality exists.
#

current_file = inspect.getfile(inspect.currentframe())
current_dir = os.path.dirname(os.path.abspath(current_file))

EXAMPLE_APPS = {
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
# Strategies
# ==========
#
# Default deployment strategies for various circumstances.
#

env.strategies = {
  'git': strategy_git,
  'symlink': strategy_symlink
}


def process_env_args(args):
  """
  A DRY way to ensure required Fabric environment vars are present and set on
  the runtime env variable.
  """

  # set on env
  for arg in args:
    if args[arg] is None:
      print(red("".join(["Missing argument '", arg, "'"])))
      sys.exit()
    env[arg] = args[arg]

  # verify role config
  if env.role not in env.roleconfig:
    print(red("Role must be configured in env.roleconfig!"))

  # set hosts
  if 'role' in args:
    env.hosts = env.roledefs[args['role']]

  # merge role config over defaults
  for role in env.roleconfig:
    tmp = ROLE_DEFAULTS.copy()
    tmp.update(env.roleconfig[role])
    env.roleconfig[role] = tmp
    del tmp

  # merge app config over defaults
  EXAMPLE_APPS.update(env.apps)
  env.apps = EXAMPLE_APPS
  for app in env.apps:
    tmp = APP_DEFAULTS.copy()
    tmp.update(env.apps[app])
    env.apps[app] = tmp
    del tmp

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

def install_sources(items):
  """ ... """
  print(yellow("Adding sources."))
  for source in items:
    file_ensure(source['path'], owner='root')
    for line in source['lines']:
      files.append(source['path'], line, use_sudo=True)

def install_ppas(items):
  """ ... """
  print(yellow("Adding PPAs."))
  for ppa in items:
    repository_ensure_apt(ppa)

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
def setup(role=None):
  """ ... """

  process_env_args(locals())
  env.user = env.admin_user
  role_config = env.roleconfig[role]

  with mode_sudo():
    execute(task(install_pgps), role_config['pgps'])
    execute(task(install_sources), role_config['sources'])
    execute(task(install_ppas), role_config['ppas'])
    execute(task(install_pkgs), role_config['pkgs'])

    for setup_task in role_config['setup_tasks']:
      execute(setup_task)

@task
@parallel(pool_size=5)
def deploy(role=None,app=None):
  """ ... """

  process_env_args(locals())
  env.user = env.deployment_user
  app_config = env.apps[app]

  print(yellow('Deploying application: ' + app))
  execute(task(env.strategies[app_config['strategy']]), app, app_config);

@task
@parallel(pool_size=5)
def deploy_examples(role=None):
  """
  This task deploys the various example apps to the listed web servers - these
  apps include NodeJS, Rack, WSGI, and PHP samples to help ensure all app types
  are working as expected.
  """

  process_env_args(locals())
  env.user = env.deployment_user

  for app in EXAMPLE_APPS:
    execute('deploy', role, app)
