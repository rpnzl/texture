""" ... """

import collections

from fabric.api import abort, execute, task as fabric_task

from texture.state import env


def update(d, u):
  """
  Util for deep updates of dicts.
  """
  for k, v in u.iteritems():
    if isinstance(v, collections.Mapping):
      r = update(d.get(k, {}), v)
      d[k] = r
    else:
      d[k] = u[k]
  return d


def task(callable):
  """
  Wraps a Fabric `task` decorator with some extra `env` var processing to
  ensure custom configuration is collapsed over defaults.

  env.role_config[role] <-- role_defaults <-- env.role_config[role]
  env.app_config[app] <-- app_defaults  <-- strategy_defaults <-- env.app_config[app]
  """
  def wrapped(*args, **kwargs):
    for role in env.roledefs:
      config = env.role_defaults.copy()
      update(config, env.role_config[role] if role in env.role_config else {})
      env.role_config[role] = config
    for app in env.app_config:
      config = env.app_defaults.copy()
      if 'strategy' in env.app_config[app]:
        strategy = env.strategies[env.app_config[app]['strategy']]
        update(config, strategy['defaults'])
      update(config, env.app_config[app])
    execute(fabric_task(callable), *args, **kwargs)
  wrapped.__name__ = callable.__name__
  wrapped.__doc__ = callable.__doc__
  return fabric_task(wrapped)


def subtask(callable):
  """ ... """
  env.subtasks[callable.__name__] = callable
  return callable


def strategy(defaults):
  """
  Defines deployment strategies on the env variable for use in the deploy
  task.
  """
  def Strategy(method):
    env.strategies[method.__name__] = {
      'defaults': defaults,
      'function': method
    }
    return method
  if callable(defaults):
    method = defaults
    defaults = {}
    return Strategy(method)
  return Strategy
