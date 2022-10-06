# nvanbaak 6 Oct 22
# given side length of a tetrahedron of cannonballs, output total cannonballs

# STRATEGY
#   Each level of the tetrahedron is a triangle
#   Number of cannonballs in a triangle of size n = 1 + ... + n
#   But we don't wanna do that on every level, so we'll use DP to store old results

import sys

num_lines = int(sys.stdin.readline().strip())
for input in range(num_lines):

    levels = []
    n = int(sys.stdin.readline().strip())
    total = 0

    for level in range(n):
        if level == 0:
            levels.append(1)
            total = 1
        else:
            # the area of a triangle of side length n is equal to
            # n plus the area of a triangle with side length n-1
            prev_level = levels[level-1]
            curr_level = prev_level + level + 1
            levels.append(curr_level)
            total += curr_level

    print(total)