# from fabric.api import env, put, run
# from cuisine import *
#
# def strategy_git(name, config):
#   print('deploying with git strategy')
#   app_dir = '/www/apps/' + name
#   dir_ensure(app_dir)
#   dir_ensure(app_dir + '/releases')
#   dir_ensure(app_dir + '/shared')
#   releases = run('ls ' + app_dir + '/releases').split()
#   release_number = (int(releases[-1]) if len(releases) else 0) + 1
#
#   # Limit release directories
#   if config['max_releases'] is not None:
#     max_releases = config['max_releases']
#   else:
#     max_releases = env.max_releases
#
#   if release_number > 0 and len(releases) > max_releases:
#     for old in releases[:(len(releases) - max_releases)]:
#       dir_remove(app_dir + '/releases/' + old)
#
#   dir_ensure(app_dir + '/releases/' + str(release_number))
#   put(env.apps[name]['local_path'] + '/*', app_dir + '/releases/' + str(release_number))
#   dir_ensure(app_dir + '/releases/' + str(release_number) + '/tmp')
#   file_link(app_dir + '/releases/' + str(release_number), app_dir + '/current')
#
# def strategy_symlink(name, config):
#   print('deploying symlink')


from texture.decorators import strategy


@strategy
def git():
  """ ... """
  print('this is git 1')


@strategy
def rsync():
  """ ... """
  pass


@strategy
def symlink():
  """ ... """
  pass
