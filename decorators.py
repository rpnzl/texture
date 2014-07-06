""" ... """

from texture.state import env


def texture_task(callable):
  """ ... """
  env.texture_tasks[callable.__name__] = callable
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
