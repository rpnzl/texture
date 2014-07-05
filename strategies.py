""" ... """

import os

from cuisine import *
from fabric.api import put, run
from fabric.colors import yellow

from texture.decorators import strategy
from texture.state import env


@strategy({
  'branch': 'master',
  'remote_base_path': '~'
})
def git(config):
  """ ... """
  print('GIT DEPLOY:', config)


@strategy({
  'remote_base_path': '~'
})
def copy(config):
  """
  Copy the application directory up to the servers directly without any VCS.
  """
  config['remote_path'] = os.path.join(config['remote_base_path'], config['name'])
  config['release_path'] = os.path.join(config['remote_path'], 'releases')
  config['shared_path'] = os.path.join(config['remote_path'], 'shared')

  dir_ensure(config['remote_path'])
  dir_ensure(config['release_path'])
  dir_ensure(config['shared_path'])

  releases = map(int, run('ls ' + config['release_path']).split())
  releases.sort()

  current = (releases[-1] if len(releases) else 0)
  new_release_path = os.path.join(config['release_path'], str(current + 1))
  dir_ensure(new_release_path)

  put(os.path.join(config['local_path'], '*'), new_release_path)
  dir_ensure(os.path.join(new_release_path, 'tmp'))
  file_link(new_release_path, os.path.join(config['remote_path'], 'current'))

  releases.append(current + 1)
  if len(releases) > env.max_releases:
    for old_release in releases[:(len(releases) - env.max_releases)]:
      dir_remove(os.path.join(config['release_path'], str(old_release)))


@strategy
def symlink(config):
  """ ... """
  print('SYM DEPLOY:', config)
