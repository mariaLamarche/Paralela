import sys
import os

# 🔥 FIX IMPORT (para encontrar /core)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import numpy as np
from core.model import update_grid, INFECTED

def simulate(days, size, params, save_grids=False, output_dir="output"):

    grid = np.zeros((size, size), dtype=int)
    grid[size//2, size//2] = INFECTED

    results = []

    if save_grids:
        os.makedirs(output_dir, exist_ok=True)

    for day in range(days):

        # 🔥 guardar grid para visualización
        if save_grids:
            np.save(os.path.join(output_dir, f"grid_day_{day:03d}.npy"), grid)

        S = (grid == 0).sum()
        I = (grid == 1).sum()
        R = (grid == 2).sum()

        results.append([day, int(S), int(I), int(R)])

        # 🔥 usar modelo compartido
        grid = update_grid(grid, params)

    return results