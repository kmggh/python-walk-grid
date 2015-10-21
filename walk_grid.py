# Copyright (c) 2015 by Ken Guyton.  All Rights Reserved.

"""Solve the grid walking problem.

Each square has a cost in food and the challenge is to walk from the
upper left corner to lower right by having the least food left over
(zero is ideal) but not run out.

The main function of the Walker is to find the optimal path, if there
is one, and to report the food left over.
"""

from __future__ import print_function


class Error(Exception):
  """All Walk Grid errors."""


class EnumError(Error):
  """An enumerated object value is not acceptable."""


class BoundError(Error):
  """A value exceeds the square's boundaries."""


class NotDirectionError(Error):
  """This is not a valid direction."""


class OutOfFood(Error):
  """Out of food at the current position, after consume."""


class DirEnum(object):
  """An enumerated object for step directions."""

  def __init__(self, direction):
    """Check the direction."""

    if direction not in ('down', 'right'):
      raise EnumError('{0} is not an allowed value.'.format(direction))

    self.value = direction

  def __eq__(self, other_dir):
    """Check the equality of directions."""

    return self.value == other_dir.value

  def __ne__(self, other_dir):
    """Check the inequality of directions."""

    return self.value != other_dir.value


DOWN = DirEnum('down')
RIGHT = DirEnum('right')


class Walker(object):
  """Walk a grid class to find hte competition."""

  def __init__(self, grid):
    """Initialize with a grid.

    Note that the position is (i, j) where i is the coordinate in  the
    x-direction and j is the coordinate in the y-direction.  However
    the grid coordinate indices are grid[j][i] where the vertical index
    is first.

    The consumed attribute tracks how much cost has accumulated over walking
    a path.  It's the same as the total amount of food that's been consumed.

    Args:
      grid: list of list of int.  The lists should all be the same size
        and represent a grid of int values.  The upper left, grid[0][0]
        should be 0.
      food: int.  The starting amount of food.
    """

    assert len(grid) == len(grid[0]), 'Grid is not a square.'
    assert grid[0][0] == 0

    self.size = len(grid)
    self.grid = grid
    self.consumed = 0
    self.position = (0, 0)

  def copy(self):
    """Make a copy."""

    walker = Walker(self.grid)
    walker.consumed = self.consumed
    walker.position = self.position

    return walker

  def in_bound(self, value):
    """Check that the coordinate is within the grid bound."""

    return value >= 0 and value < self.size

  def step(self, direction):
    """Move either down or right."""

    if direction == DOWN:
      old_i, old_j = self.position
      new_j = old_j + 1
      if self.in_bound(new_j):
        self.position = old_i, new_j
      else:
        raise BoundError('Value {0} is not in bounds.'.format(new_j))

    elif direction == RIGHT:
      old_i, old_j = self.position
      new_i = old_i + 1
      if self.in_bound(new_i):
        self.position = new_i, old_j
      else:
        raise BoundError('Value {0} is not in bounds.'.format(new_i))

    else:
      raise NotDirectionError(
          'Value {0} is not a valid direction.'.format(direction))

  def consume(self):
    """Eat the food at the current position."""

    pos_i, pos_j = self.position
    self.consumed += self.grid[pos_j][pos_i]

  def at_end(self):
    """Indicate if  we have reached the bottom right corner."""

    pos_i, pos_j = self.position
    return pos_i == (self.size - 1) and pos_j == (self.size - 1)


class Collector(object):
  """Walk all possible paths and collect the set of food costs."""

  def __init__(self, grid):
    """Initialize the grid anf food.

    Args:
      grid: list of list of int.  The lists should all be the same size
        and represent a grid of int values.  The upper left, grid[0][0]
        should be 0.
      food: int.  The starting amount of food.
    """

    self.grid = grid
    self.costs = None

  def collect_costs_recursive(self, walker):
    """Walk all paths and accumulate costs.

    The walker has *already consumed* the food at this current position.

    Args:
      walker: Walker.  A walker that's walking these paths.
      costs: set. A set of accumulated costs.
    Returns:
      A set of costs accumulated on all possible paths from the
      walker's current position.
    """

    costs = set([])

    if walker.at_end():
      costs.add(walker.consumed)
      return costs

    walker_right = walker.copy()

    try:
      walker_right.step(RIGHT)
    except BoundError:
      pass
    else:
      walker_right.consume()
      costs_right = self.collect_costs_recursive(walker_right)
      costs = costs.union(costs_right)

    walker_down = walker.copy()

    try:
      walker_down.step(DOWN)
    except BoundError:
      pass
    else:
      walker_down.consume()
      costs_down = self.collect_costs_recursive(walker_down)
      costs = costs.union(costs_down)

    return costs

  def collect_costs(self):
    """Collect the set of costs for all paths.

    This method really just starts up the recursive search.
    """

    return self.collect_costs_recursive(Walker(self.grid))

  def least_left(self, food):
    """Find a food cost which has the least food left over.

    If there is not a cost that's smaller than the food supply, i.e., no
    solution, then return -1.
    """

    if self.costs is None:
      self.costs = self.collect_costs()

    left_overs = [(food - x) for x in self.costs if x <= food]

    if not left_overs:
      return -1
    else:
      return min(left_overs)


def answer(grid, food):
  """For the problem, return the least left or -1 if no solution.

  Args:
    grid: list of list of int.  The lists should all be the same size
      and represent a grid of int values.  The upper left, grid[0][0]
      should be 0.
    food: int.  The starting amount of food.
  Returns:
    The smallest amount, int, of left-over food when the path is chosen that
    consumed the most food without running out.  If there is no solution
    then -1 is returned.
  """

  collector = Collector(grid)
  return collector.least_left(food)
