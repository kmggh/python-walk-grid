Grid Walk
=========

Ken Guyton<br />
Wed 2015-10-20 23:41:00 -0400

This is another programming assignment from Brian.  The original
story, at told to me by him but I believe he said it's from a
programming challenge.

Essentials
----------

* Cross an NxN grid from upper left to lower right.
* Only move down, right.
* Food is consumed in each square (except first upper left).
* Find path that consumes the most food, leftover = 0 is "perfect."
* If all is consumed before reaching lower right, return -1.  (Failure).


Solution
--------

Follow each path through the grid.  Compute all "path costs."   For a
given starting food amount, find the highest path cost that doesnt' go
over.  If no solution, return -1.   Else, subtract highest and return
difference from food start value (leftovers).


To Run
------

    ./solution.py
    ./random_solution.py


To Test
-------

    ./test_walk_grid.py



Bugs/Next Steps
---------------

Add an option to random_solution.py to allow setting the grid size.
Maybe all parameters.

Prune the search to make the solutions faster.  Track the minimum
solution and abort branches that exceed it.  This is really the main
goal of this exercise.


Original Story
--------------


### Save Beta Rabbit


Oh no! The mad Professor Boolean has trapped Beta Rabbit in an NxN
grid of rooms. In the center of each room (except for the top left
room) is a hungry zombie. In order to be freed, and to avoid being
eaten, Beta Rabbit must move through this grid and feed the zombies.

Beta Rabbit starts at the top left room of the grid. For each room in
the grid, there is a door to the room above, below, left, and
right. There is no door in cases where there is no room in that
direction. However, the doors are locked in such a way that Beta
Rabbit can only ever move to the room below or to the right. Once Beta
Rabbit enters a room, the zombie immediately starts crawling towards
him, and he must feed the zombie until it is full to ward it off.
Thankfully, Beta Rabbit took a class about zombies and knows how many
units of food each zombie needs be full.

To be freed, Beta Rabbit needs to make his way to the bottom right
room (which also has a hungry zombie) and have used most of the
limited food he has. He decides to take the path through the grid such
that he ends up with as little food as possible at the end.

Write a function answer(food, grid) that returns the number of units
of food Beta Rabbit will have at the end, given that he takes a route
using up as much food as possible without him being eaten, and ends at
the bottom right room. If there does not exist a route in which Beta
Rabbit will not be eaten, then return -1.

Food is the amount of food Beta Rabbit starts with, and will be a
positive integer no larger than 200.

Grid will be a list of N elements. Each element of grid will itself be
a list of N integers each, denoting a single row of N rooms. The first
element of grid will be the list denoting the top row, the second
element will be the list denoting second row from the top, and so on
until the last element, which is the list denoting the bottom row. In
the list denoting a single row, the first element will be the amount
of food the zombie in the left-most room in that row needs, the second
element will be the amount the zombie in the room to its immediate
right needs and so on. The top left room will always contain the
integer 0, to indicate that there is no zombie there.

The number of rows N will not exceed 20, and the amount of food each
zombie requires will be a positive integer not exceeding 10.


### Test cases


Inputs:
   (int) food = 7
   (int) grid = [[0, 2, 5], [1, 1, 3], [2, 1, 1]]
Output:
   (int) 0

Inputs:
   (int) food = 12
   (int) grid = [[0, 2, 5], [1, 1, 3], [2, 1, 1]]
Output:
   (int) 1
