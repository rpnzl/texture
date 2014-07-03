""" ... """

import os

from cuisine import *
from fabric.api import put, run
from fabric.colors import yellow

from texture.decorators import strategy
# from texture.deploy_utils import extend_app_config, get_release_list
from texture.state import env


@strategy
def git(config):
  """ ... """
  defaults = {'branch': 'master'}
  pass


@strategy
def copy(config):
  """
  Copy the application directory up to the servers directly without any VCS.
  """

  print(config)
  # extend_app_config(config)
  # releases = get_release_list(config)
  #
  # current = (releases[-1] if len(releases) else 0)
  # new_release_path = os.path.join(config['release_path'], str(current + 1))
  # dir_ensure(new_release_path)
  #
  # put(os.path.join(config['local_path'], '*'), new_release_path)
  # dir_ensure(os.path.join(new_release_path, 'tmp'))
  # file_link(next_release_dir, os.path.join(config['remote_path'], 'current'))
  #
  # prune_releases(config)


@strategy
def symlink(config):
  """ ... """
  pass
