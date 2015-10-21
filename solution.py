#!/usr/bin/env python
# Copyright (c) 2015 by Ken Guyton.  All Rights Reserved.

"""Run the solutions originally specified by the problem."""

from __future__ import print_function

import walk_grid


def main():
  """Compute the answer for the given grid and food amounts."""

  grid = [[0, 2, 5], [1, 1, 3], [2, 1, 1]]

  assert walk_grid.answer(grid, 7) == 0
  assert walk_grid.answer(grid, 12) == 1

  print('Passed!')


if __name__ == '__main__':
  main()
