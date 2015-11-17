#!/usr/bin/env python
# Copyright (c) 2015 by Ken Guyton.  All Rights Reserved.

"""Create a random grid and compute the solution."""

from __future__ import print_function

import argparse
import walk_grid
import random

MAX_GRID_SIZE = 20
MAX_FOOD = 200
MAX_ROOM_FOOD = 10


def get_args():
  """Parse command line arguments."""

  parser = argparse.ArgumentParser()
  parser.add_argument('--grid_size', default=11, type=int,
                      help='The size of each side of the grid.')
  parser.add_argument('--food', default=150, type=int,
                      help='Amount of food.')
  return parser.parse_args()


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

  opts = get_args()

  if opts.food > MAX_FOOD:
    print('WARNING, you have exceeded the MAX FOOD size: {0}'.format(MAX_FOOD))
  if opts.grid_size > MAX_GRID_SIZE:
    print('WARNING, you have exceeded the MAX GRID SIZE: {0}'.format(
        MAX_GRID_SIZE))

  print('Food: {0}.'.format(opts.food))
  print('Grid size: {0}.'.format(opts.grid_size))

  grid = create_grid(opts.grid_size)
  print('\nThe Grid...\n')
  print_grid(grid)
  print()

  least_left, steps = walk_grid.answer_and_steps(grid, opts.food)

  print('\nResult: {0} with steps {1}.'.format(least_left, steps))


if __name__ == '__main__':
  main()
