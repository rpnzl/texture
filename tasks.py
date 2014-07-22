"""
Top-level tasks to be used within a Fabfile.
"""

import os
import sys
import StringIO

from cuisine import *
from fabric import contrib
from fabric.api import abort, execute, get, put, run, sudo, task as fabric_task
from fabric.colors import yellow

from texture.decorators import subtask, task
from texture.state import env


@task
def setup():
  """
  Sets up the specified roles in sequence based on env.role_config
  Fabric 1.x is too limited to allow for parallel role configuration -- this
  should change with the release of Fabric 2.x. Check out this Github issue
  for more info...

  https://github.com/fabric/fabric/issues/361

  # ensure hostname exists in hosts due to AWS inconsistency
  # host_string = '127.0.1.1 ' + sudo('hostname').split('\r\n').pop()
  # contrib.files.append('/etc/hosts', host_string, use_sudo=True)
  """
  env.user = env.admin_user
  for role in env.roles:
    with mode_sudo():
      defaults = ['install_pgps',
                  'install_sources',
                  'install_ppas',
                  'install_pkgs',
                  'setup_deploy_user']
      for subtask in defaults:
        execute(fabric_task(env.subtasks[subtask]), env.role_config[role])
      for subtask in env.role_config[role]['subtasks']['setup']:
        execute(fabric_task(env.subtasks[subtask]), env.role_config[role])


@task
def deploy(app):
  """ ... """
  env.user = env.deploy_user
  if 'strategy' in env.app_config[app]:
    strategy_name = env.app_config[app]['strategy']
  else:
    strategy_name = env.strategy
  strategy = env.strategies[strategy_name]
  execute(fabric_task(strategy['function']), app)


@subtask
def install_pgps(config):
  """ ... """
  items = config['pgps']
  if not items:
    print(yellow("No PGPs specified."))
    return
  print(yellow("Installing PGPs."))
  for pgp in items:
    sudo(" ".join([
      "apt-key adv --keyserver",
      pgp['server'],
      "--recv-keys",
      pgp['key']
    ]))


@subtask
def install_sources(config):
  """ ... """
  items = config['sources']
  if not items:
    print(yellow("No sources specified."))
    return
  print(yellow("Adding sources."))
  for source in items:
    file_ensure(source['path'], owner='root')
    for line in source['lines']:
      contrib.files.append(source['path'], line, use_sudo=True)


@subtask
def install_ppas(config):
  """ ... """
  items = config['ppas']
  if not items:
    print(yellow("No PPAs specified."))
    return
  print(yellow("Adding PPAs."))
  for ppa in items:
    repository_ensure_apt(ppa)


@subtask
def install_pkgs(config):
  """ ... """
  items = config['pkgs']
  if not items:
    print(yellow("No packages specified."))
    return
  print(yellow("Installing packages."))
  package_update()
  package_upgrade()
  package_ensure(' '.join(items))


@subtask
def setup_deploy_user(config):
  home_dir = '~' + env.deploy_user
  user_ensure(env.deploy_user, shell='/bin/bash')
  dir_ensure(home_dir + '/.ssh', mode='0700',
    owner=env.deploy_user, group=env.deploy_user)
  file_ensure(home_dir + '/.ssh/authorized_keys', mode='0600',
    owner=env.deploy_user, group=env.deploy_user)

  # Transfer SSH key
  f = StringIO.StringIO()
  get('~/.ssh/authorized_keys', f)
  contrib.files.append(home_dir + '/.ssh/authorized_keys', f.getvalue(), use_sudo=True)
