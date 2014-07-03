"""
...
"""

import os

from cuisine import *

from texture.state import env


def get_release_list(config):
  """
  ...
  """
  path = config['']
  releases = map(int, run('ls ' + config['release_path']).split())
  releases.sort()
  return releases


def process_app_config(config):
  """
  Extends the given app config with useful variables.
  """
  pass

  # 'local_path': None,
  # 'remote_base_path': '/www/apps',
  # 'shared_dirs': [],
  # 'strategy': 'copy'
  # config['name'] = name
  # base_path = config['remote_base_path']
  # config['remote_path'] = os.path.join(base_path, config['name'])
  # config['release_path'] = os.path.join(config['remote_path'], 'releases')
  # config['shared_path'] = os.path.join(config['remote_path'], 'shared')


# def ensure_app_structure(config):
#   """
#   Ensures the app structure exists.
#   """
#   app_path = os.path.join(config['remote_path'], config['name'])
#   rel_path = os.path.join(app_path, 'releases')
#   sh_path = os.path.join(app_path, 'shared')
#
#   dir_ensure(rel_path, recursive=True)
#   dir_ensure(sh_path, recursive=True)


# def prune_releases(config):
#   """ ... """
#   releases = get_release_list(config)
#   if len(releases) > env.max_releases:
#     for old in releases[:(len(releases) - env.max_releases)]:
#       dir_remove(os.path.join(config['release_path'], str(old)))
