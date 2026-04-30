import numpy as np

SUSCEPTIBLE = 0
INFECTED = 1
RECOVERED = 2

def update_grid(grid, params):
    I_grid = (grid == INFECTED).astype(int)

    padded = np.pad(I_grid, 1, mode='constant')

    neighbors = (
        padded[:-2, :-2] + padded[:-2, 1:-1] + padded[:-2, 2:] +
        padded[1:-1, :-2] + padded[1:-1, 2:] +
        padded[2:, :-2] + padded[2:, 1:-1] + padded[2:, 2:]
    )

    prob = 1.0 - (1.0 - params["beta"])**neighbors

    rand_S = np.random.rand(*grid.shape)
    rand_I = np.random.rand(*grid.shape)

    new_inf = (grid == SUSCEPTIBLE) & (rand_S < prob)
    new_rec = (grid == INFECTED) & (rand_I < params["gamma"])

    grid[new_inf] = INFECTED
    grid[new_rec] = RECOVERED

    return grid
