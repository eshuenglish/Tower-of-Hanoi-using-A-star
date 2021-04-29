# Tower-of-Hanoi-using-A-star
This Repo contains my project on A-star use for Tower of Hanoi

# Project: Tower of Hanoi
Goal: You will reflect upon the search algorithms learned during the lectures and implement two of them to solve the Tower of Hanoi.

# Setting of the game:

1) The Tower of Hanoi is a puzzle game with usually 3 pegs and a fixed number of disks. For this project, we will use 4 pegs. Consider n > 0 number of discs.
2) Initial state: At the start, all the disks are in the leftmost peg, with the largest disk on the bottom and the smallest on the top.
3) Goal state: All disks are moved over to the rightmost peg.

# Rules of the game:
1) You can only move one disk to any other peg in each move, and you can only move the top disk on a peg.
2) The top disk of any peg can be moved to the top disk of any other peg, with the restriction that you cannot move a larger disk on top of a smaller disk (i.e., disks can only be moved to empty pegs or on top of larger disks).
3) This is a unit-cost domain, all moves cost the same. Path cost is its length
