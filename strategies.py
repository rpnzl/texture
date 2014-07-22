""" ... """

import os

from cuisine import *
from fabric.api import put, run
from fabric.colors import yellow

from texture.decorators import strategy
from texture.state import env


REMOTE_BASE_DIR = '/www/apps'

@strategy({'branch': 'master'})
def git(app_name):
  """ ... """
  print('GIT DEPLOY:', config)


@strategy
def copy(app_name):
  """
  Copy the application directory up to the servers directly without any VCS.
  """
  config['remote_path'] = os.path.join(REMOTE_BASE_DIR, config['name'])
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


@strategy({'target': None})
def symlink(app_name):
  """ ... """
  if not config['target']:
    print(red('A target MUST be defined!'))
  file_link(config['target'], os.path.join(REMOTE_BASE_DIR, config['name']))
