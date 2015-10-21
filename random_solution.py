#!/usr/bin/env python
# Copyright (c) 2015 by Ken Guyton.  All Rights Reserved.

"""Create a random grid and compute the solution."""

from __future__ import print_function

import walk_grid
import random

MAX_GRID_SIZE = 20
MAX_FOOD = 200
MAX_ROOM_FOOD = 10


def create_grid(grid_size):
  """Randomly create a grid."""

  grid = []

  for j in range(grid_size):
    grid.append([])
    for unused_i in range(grid_size):
      grid[j].append(random.randrange(MAX_ROOM_FOOD + 1))

  grid[0][0] = 0

  return grid


def print_grid(grid):
  """Print out a grid."""

  for row in grid:
    for num in row:
      print(' {0:2d}'.format(num), end='')
    print()


def main():
  """Compute the answer for the given grid and food amounts."""

  food = random.randrange(MAX_FOOD + 1)
  print('Food: {0}.'.format(food))

  grid_size = random.randrange(1, MAX_GRID_SIZE + 1)
  print('Grid size: {0}.'.format(grid_size))

  grid = create_grid(grid_size)

  print('\nThe Grid...\n')
  print_grid(grid)
  print()

  print('Result: {0}.'.format(walk_grid.answer(grid, food)))


if __name__ == '__main__':
  main()
