# Copyright (c) 2015 by Ken Guyton.  All Rights Reserved.

"""Solve the grid walking problem.

Each square has a cost in food and the challenge is to walk from the
upper left corner to lower right by having the least food left over
(zero is ideal) but not run out.

The main function of the Walker is to find the optimal path, if there
is one, and to report the food left over.
"""

from __future__ import print_function

import sys

STEP_REPORT = 5000


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
  """Walk a grid class to find hte competition.

  The step_counter tracks how many steps have been taken.
  """

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
    self.step_counter = 0

  def copy(self):
    """Make a copy.

    Note that the step_counter *is not* copied but reset to zero.
    """

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

    self.step_counter += 1

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
    self.steps = 0

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
      self.steps += walker_right.step_counter

    walker_down = walker.copy()

    try:
      walker_down.step(DOWN)
    except BoundError:
      pass
    else:
      walker_down.consume()
      costs_down = self.collect_costs_recursive(walker_down)
      costs = costs.union(costs_down)
      self.steps += walker_down.step_counter

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

  collector = TrimCollector(grid)
  return collector.least_left(food)


def answer_and_steps(grid, food):
  """Return the least left or -1 and the steps taken.

  Args:
    grid: list of list of int.  The lists should all be the same size
      and represent a grid of int values.  The upper left, grid[0][0]
      should be 0.
    food: int.  The starting amount of food.
  Returns:

    A tuple pair where the first element is smallest amount, int, of
    left-over food when the path is chosen that consumed the most food
    without running out.  If there is no solution then -1 is returned.
    The second element is the amount of steps it took through the grid
    to find the solution.
  """

  collector = TrimCollector(grid)
  return collector.least_left(food), collector.steps


class TrimCollector(Collector):
  """Walk all possible paths and find the cheapest cost.

  This subclass of Collector trims the tree walk by not pursuing
  paths that don't have a better solution.
  """

  def __init__(self, grid):
    """Initialize the grid anf food.

    Args:
      grid: list of list of int.  The lists should all be the same size
        and represent a grid of int values.  The upper left, grid[0][0]
        should be 0.
    """

    super(TrimCollector, self).__init__(grid)

  def perfect_solution(self, best, food):
    """Check whether we've already found a perfect solution.

    In this case we don't need to pursue any more.

    Returns:
      Boolean True if best == food.
    """

    return best == food

  def consumed_already_worse_or_equal(self, best, new):
    """Check a new consumed value against a best.

    Returns:
      A boolean True value if  the new value is already less than the
      best or equal, i.e., not potentially better.  After all, we're
      trying to consume as much food as possible without going over.
    """

    if best is None:
      return False
    else:
      return new <= best

  def step_report(self, steps):
    """Report the step count."""

    if not steps % STEP_REPORT:
      sys.stdout.write('{0}...'.format(steps))
      sys.stdout.flush()

  def collect_trim_recursive(self, walker, food):
    """Walk trimmed paths and find the largest cost that <= target.

    The walker has *already consumed* the food at this current position.

    Args:
      walker: Walker.  A walker that's walking these paths.
      costs: set. A set of accumulated costs.
      food: int. The amount of food that must be consumed.  The walker
        has to consume >= this amount, i.e., the cost must.
    Returns:
      The minimum cost that is >= the food value else None.
    """

    if walker.at_end():
      if walker.consumed <= food:
        return walker.consumed
      else:
        return None

    walker_right = walker.copy()

    try:
      walker_right.step(RIGHT)
    except BoundError:
      cost_right = None
    else:
      walker_right.consume()
      cost_right = self.collect_trim_recursive(walker_right, food)
      self.steps += walker_right.step_counter
      self.step_report(self.steps)

    walker_down = walker.copy()

    try:
      walker_down.step(DOWN)
    except BoundError:
      cost_down = None
    else:
      walker_down.consume()

      # This is where we trim the tree walk.
      if self.perfect_solution(cost_right, food):
        cost_down = None
      elif self.consumed_already_worse_or_equal(cost_right,
                                                walker_down.consumed):
        cost_down = None
      else:
        cost_down = self.collect_trim_recursive(walker_down, food)
        self.steps += walker_down.step_counter
        self.step_report(self.steps)

    if cost_right is not None and cost_down is not None:
      return max(cost_right, cost_down)
    elif cost_right is not None:
      return cost_right
    elif cost_down is not None:
      return cost_down
    else:
      return None

  def least_left(self, food):
    """Find a food cost which has the least food left over.

    If there is not a cost that's smaller than the food supply, i.e., no
    solution, then return -1.
    """

    min_cost = self.collect_trim_recursive(Walker(self.grid), food)

    if min_cost is None:
      return -1
    else:
      return food - min_cost
