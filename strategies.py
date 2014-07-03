""" ... """

import os

from cuisine import *
from fabric.api import put, run
from fabric.colors import yellow

from texture.decorators import strategy
from texture.state import env


@strategy
def git(name, config):
  """ ... """
  defaults = {'branch': 'master'}


@strategy
def copy(name, config):
  """
  Copy the application directory up to the servers directly without any VCS.
  """

  app_dir = os.path.join(config['remote_path'], name)
  dir_ensure(os.path.join(app_dir, 'releases'), recursive=True)
  dir_ensure(os.path.join(app_dir, 'shared'), recursive=True)

  # get current release info
  releases = map(int, run('ls ' + os.path.join(app_dir, 'releases')).split())
  releases.sort()

  current_release = (releases[-1] if len(releases) else 0)
  next_release = current_release + 1

  # deploy new release
  next_release_dir = os.path.join(app_dir, 'releases', str(next_release))
  dir_ensure(next_release_dir)
  put(os.path.join(config['local_path'], '*'), next_release_dir)
  dir_ensure(os.path.join(next_release_dir, 'tmp'))
  file_link(next_release_dir, os.path.join(app_dir, 'current'))

  # delete extra releases
  if current_release > 0 and (len(releases) + 1) > env.max_releases:
    for old in releases[:(len(releases) - env.max_releases + 1)]:
      dir_remove(os.path.join(app_dir, 'releases', str(old)))


@strategy
def symlink(name, config):
  """ ... """
  pass
