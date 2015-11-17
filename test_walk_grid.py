#!/usr/bin/env python
# Copyright (c) 2015 by Ken Guyton.  All Rights Reserved.

"""The test grid:

  0  2  5
  1  1  3
  2  1  1

"""


import unittest
import walk_grid

GRID = [[0, 2, 5], [1, 1, 3], [2, 1, 1]]
FOOD = 12
STEPS = 18

SMALL_GRID = [[0, 2], [1, 3]]
SMALL_COSTS = set([4, 5])
SMALL_STEPS = 4


class _BadDirection(object):
  """A bad direction for testing direction type."""

  def __init__(self, value):
    """Set the value."""

    self.value = value


class TestWalker(unittest.TestCase):
  def setUp(self):
    self.walker = walk_grid.Walker(GRID)

  def test_create(self):
    self.assertNotEqual(self.walker, None)
    self.assertEqual(self.walker.position, (0, 0))
    self.assertEqual(self.walker.consumed, 0)
    self.assertEqual(self.walker.step_counter, 0)

  def test_copy(self):
    self.walker.position = (1, 2)
    self.walker.consumed = 5
    self.walker.step_counter = 4
    walker2 = self.walker.copy()
    self.assertEqual(walker2.position, (1, 2))
    self.assertEqual(walker2.consumed, 5)
    self.assertEqual(walker2.grid, GRID)
    self.assertEqual(walker2.step_counter, 0)

  def test_assert_square(self):
    asymetric_grid = [[0, 2], [1, 1], [2, 1]]
    self.assertRaises(AssertionError, walk_grid.Walker, asymetric_grid)

  def test_assert_upper_left_zero(self):
    non_zero_grid = [[5, 2], [1, 1], [2, 1]]
    self.assertRaises(AssertionError, walk_grid.Walker, non_zero_grid)

  def test_in_bound(self):
    self.assertTrue(self.walker.in_bound(0))
    self.assertTrue(self.walker.in_bound(1))
    self.assertFalse(self.walker.in_bound(3))
    self.assertFalse(self.walker.in_bound(-1))

  def test_step_down(self):
    self.walker.step(walk_grid.DOWN)
    self.assertEqual(self.walker.position, (0, 1))
    self.assertEqual(self.walker.step_counter, 1)

  def test_step_down_error(self):
    self.walker.position = (0, 2)
    self.assertRaises(walk_grid.BoundError, self.walker.step, walk_grid.DOWN)

  def test_step_right(self):
    self.walker.step(walk_grid.RIGHT)
    self.assertEqual(self.walker.position, (1, 0))
    self.assertEqual(self.walker.step_counter, 1)

  def test_step_right_error(self):
    self.walker.position = (2, 0)
    self.assertRaises(walk_grid.BoundError, self.walker.step, walk_grid.RIGHT)

  def test_direction_error(self):
    self.assertRaises(walk_grid.NotDirectionError, self.walker.step,
                      _BadDirection('other'))

  def test_consume(self):
    self.walker.position = (2, 1)
    self.walker.consume()

  def test_walk_path(self):
    self.walker.step(walk_grid.RIGHT)
    self.walker.consume()
    self.walker.step(walk_grid.RIGHT)
    self.walker.consume()
    self.walker.step(walk_grid.DOWN)
    self.walker.consume()
    self.walker.step(walk_grid.DOWN)
    self.walker.consume()
    self.assertEqual(self.walker.consumed, 11)
    self.assertEqual(self.walker.step_counter, 4)

  def test_at_end(self):
    self.assertFalse(self.walker.at_end())

    self.walker.position = (1, 1)
    self.assertFalse(self.walker.at_end())

    self.walker.position = (2, 2)
    self.assertTrue(self.walker.at_end())


class TestCollector(unittest.TestCase):
  def setUp(self):
    self.collector = walk_grid.Collector(GRID)

  def test_create(self):
    self.assertNotEqual(self.collector, None)
    self.assertEqual(self.collector.costs, None)

  def test_costs_recursive_small(self):
    self.collector = walk_grid.Collector(SMALL_GRID)
    walker = walk_grid.Walker(SMALL_GRID)
    self.assertEqual(self.collector.collect_costs_recursive(walker),
                     SMALL_COSTS)
    self.assertEqual(self.collector.steps, SMALL_STEPS)

  def test_costs_recursive(self):
    self.collector = walk_grid.Collector(GRID)
    walker = walk_grid.Walker(GRID)
    self.assertEqual(self.collector.collect_costs_recursive(walker),
                     set([4, 5, 6, 7, 11]))
    self.assertEqual(self.collector.steps, STEPS)

  def test_costs(self):
    self.collector = walk_grid.Collector(GRID)
    self.assertEqual(self.collector.collect_costs(), set([4, 5, 6, 7, 11]))

  def test_least_left(self):
    self.assertEqual(self.collector.least_left(12), 1)
    self.assertEqual(self.collector.least_left(8), 1)
    self.assertEqual(self.collector.least_left(9), 2)
    self.assertEqual(self.collector.least_left(11), 0)
    self.assertEqual(self.collector.least_left(4), 0)

  def test_least_left_out(self):
    self.assertEqual(self.collector.least_left(3), -1)


class TestTrimCollector(TestCollector):
  def setUp(self):
    self.collector = walk_grid.TrimCollector(GRID)

  def _test_collect_trim_recursive(self, food, best_cost, steps):
    walker = walk_grid.Walker(GRID)
    self.assertEqual(self.collector.collect_trim_recursive(walker, food),
                     best_cost)
    self.assertEqual(self.collector.steps, steps)

  def test_collect_trim_5(self):
    self._test_collect_trim_recursive(5, 5, 9)

  def test_collect_trim_6(self):
    self._test_collect_trim_recursive(6, 5, 9)

  def test_collect_trim_7(self):
    self._test_collect_trim_recursive(7, 7, 7)

  def test_collect_trim_8(self):
    self._test_collect_trim_recursive(8, 7, 7)

  def test_collect_trim_9(self):
    self._test_collect_trim_recursive(9, 7, 7)

  def test_collect_trim_10(self):
    self._test_collect_trim_recursive(10, 7, 7)

  def test_collect_trim_11(self):
    self._test_collect_trim_recursive(11, 11, 4)

  def test_collect_trim_12(self):
    self._test_collect_trim_recursive(12, 11, 4)

  def test_least_left(self):
    self.assertEqual(self.collector.least_left(8), 1)
    self.assertEqual(self.collector.least_left(9), 2)
    self.assertEqual(self.collector.least_left(11), 0)
    self.assertEqual(self.collector.least_left(4), 0)
    self.assertEqual(self.collector.least_left(7), 0)
    self.assertEqual(self.collector.least_left(12), 1)

  def test_least_left_out(self):
    self.assertEqual(self.collector.least_left(3), -1)


if __name__ == '__main__':
  unittest.main()
