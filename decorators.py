""" ... """

from texture.state import env


def strategy(callable):
  """
  Defines deployment strategies on the env
  variable for use in the deploy task.
  """
  env.strategies[callable.__name__] = callable
  return callable
