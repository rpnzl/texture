"""
Top-level tasks to be used within a Fabfile.
"""

import sys

from cuisine import *
from fabric import contrib
from fabric.api import abort, execute, parallel, put, run, task
from fabric.colors import yellow

from texture.state import env


@task
def setup():
  """
  Sets up the specified roles in sequence based on env.role_config
  Fabric 1.x is too limited to allow for parallel role configuration -- this
  should change with the release of Fabric 2.x. Check out this Github issue
  for more info...

  https://github.com/fabric/fabric/issues/361
  """

  env.user = env.admin_user

  if not env.roles:
    abort("You MUST specify a role to setup.")

  if len(env.roles) != len(env.roleconfig):
    abort("The specified roles MUST exist in env.roleconfig.")

  for role in env.roles:
    print(yellow('Running setup for: ' + role))
    role_config = env.role_defaults.copy()
    role_config.update(env.role_config[role])
    with mode_sudo():
      execute(task(install_pgps), role_config['pgps'])
      execute(task(install_sources), role_config['sources'])
      execute(task(install_ppas), role_config['ppas'])
      execute(task(install_pkgs), role_config['pkgs'])
      for setup_task in role_config['tasks']:
        execute(task(setup_task))


# @task
# @parallel(pool_size=5)
# def deploy():
#   """ ... """
#
#   env.user = env.deployment_user
#   app_config = env.apps[app]
#
#   print(yellow('Deploying application: ' + app))
#   execute(task(env.strategies[app_config['strategy']]), app, app_config);
#
#
# @task
# @parallel(pool_size=5)
# def deploy_examples():
#   """
#   This task deploys the various example apps to the listed web servers - these
#   apps include NodeJS, Rack, WSGI, and PHP samples to help ensure all app types
#   are working as expected.
#   """
#
#   env.user = env.deployment_user
#
#   for app in EXAMPLE_APPS:
#     execute('deploy', role, app)
#
# @task
# @parallel(pool_size=5)
# def deploy_symbolic_app(sym, app):
#   env.user = 'deploy'
#   if file_exists('/www/apps/' + app):
#     file_link('/www/apps/' + app, '/www/apps/' + sym)
#     run('touch /www/apps/' + sym + '/current/tmp/restart.txt')
#
#   env.user = 'ubuntu'
#   with mode_sudo():
#     run('service nginx reload')







def install_pgps(items):
  """ ... """
  if not items:
    print(yellow("No PGPs specified."))
    return
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
  if not items:
    print(yellow("No sources specified."))
    return
  print(yellow("Adding sources."))
  for source in items:
    file_ensure(source['path'], owner='root')
    for line in source['lines']:
      contrib.files.append(source['path'], line, use_sudo=True)

def install_ppas(items):
  """ ... """
  if not items:
    print(yellow("No PPAs specified."))
    return
  print(yellow("Adding PPAs."))
  for ppa in items:
    repository_ensure_apt(ppa)

def install_pkgs(items):
  """ ... """
  if not items:
    print(yellow("No packages specified."))
    return
  print(yellow("Installing packages."))
  package_update()
  package_upgrade()
  package_ensure(' '.join(items))
