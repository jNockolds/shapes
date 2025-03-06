import math

# variables:
width = 20
screen = [['◻' for _ in range(width)] for _ in range(width)]

# functions:

def grid_print(grid):
    for i in range(width):
        for j in range(width):
            print(grid[i][j], end=' ')
        print()

def circle_filter(grid, radius):
    for i in range(width):
        for j in range(width):
            if ((i - ((width - 1) / 2))**2 + (j - ((width - 1) / 2))**2) <= radius**2:
                grid[i][j] = '◼'

# main:
circle_filter(screen, width / 2)

grid_print(screen)