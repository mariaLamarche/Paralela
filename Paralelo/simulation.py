import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import numpy as np
import multiprocessing as mp
from multiprocessing import Process, Pipe, Queue
from core.model import update_grid

SUSCEPTIBLE = 0
INFECTED = 1
RECOVERED = 2

def create_grid(size):
    grid = np.zeros((size, size), dtype=int)
    center = size // 2
    grid[center, center] = INFECTED
    return grid

def worker_process(rank, cores, local_rows, cols, days, params, pipe_top, pipe_bottom, result_queue, local_grid):
    np.random.seed(42 + rank)

    data_start = 1 if rank > 0 else 0
    data_end = data_start + local_rows

    total_local_rows = local_rows + (1 if rank > 0 else 0) + (1 if rank < cores - 1 else 0)
    grid = np.zeros((total_local_rows, cols), dtype=int)
    grid[data_start:data_end, :] = local_grid

    for day in range(days):

        # ==============================
        # 1. STATS
        # ==============================
        real_data = grid[data_start:data_end, :]

        S = np.sum(real_data == SUSCEPTIBLE)
        I = np.sum(real_data == INFECTED)
        R = np.sum(real_data == RECOVERED)

        result_queue.put(('stats', rank, day, (int(S), int(I), int(R))))

        # ==============================
        # 2. ENVIAR GRID
        # ==============================
        result_queue.put(('grid', rank, day, real_data.copy()))

        # ==============================
        # 3. GHOST EXCHANGE
        # ==============================
        if rank > 0:
            pipe_top.send(grid[data_start, :].copy())
            grid[0, :] = pipe_top.recv()

        if rank < cores - 1:
            pipe_bottom.send(grid[data_end - 1, :].copy())
            grid[-1, :] = pipe_bottom.recv()

        # ==============================
        # 4. UPDATE CORRECTO
        # ==============================
        real_slice = grid[data_start:data_end, :]
        updated = update_grid(real_slice.copy(), params)
        grid[data_start:data_end, :] = updated


def simulate(days, size, params, cores=4, save_grids=False, output_dir="output"):

    global_grid = create_grid(size)

    local_rows = size // cores
    if size % cores != 0:
        raise ValueError("El tamaño debe ser divisible por cores")

    pipes = [Pipe() for _ in range(cores - 1)]
    result_queue = Queue()

    if save_grids:
        os.makedirs(output_dir, exist_ok=True)

    workers = []

    for rank in range(cores):
        pipe_top = pipes[rank-1][1] if rank > 0 else None
        pipe_bottom = pipes[rank][0] if rank < cores - 1 else None

        start = rank * local_rows
        end = (rank + 1) * local_rows

        p = Process(
            target=worker_process,
            args=(rank, cores, local_rows, size, days, params,
                  pipe_top, pipe_bottom, result_queue,
                  global_grid[start:end, :])
        )
        workers.append(p)

    for p in workers:
        p.start()

    global_results = {d: [0, 0, 0] for d in range(days)}
    grids_temp = {d: [None]*cores for d in range(days)}

    expected = cores * days * 2
    received = 0

    while received < expected:
        msg = result_queue.get()
        tipo = msg[0]

        if tipo == 'stats':
            _, rank, day, (S, I, R) = msg
            global_results[day][0] += S
            global_results[day][1] += I
            global_results[day][2] += R
            received += 1

        elif tipo == 'grid':
            _, rank, day, part = msg
            grids_temp[day][rank] = part
            received += 1

    for p in workers:
        p.join()

    # ==============================
    # GUARDAR GRIDS
    # ==============================
    if save_grids:
        for day in range(days):
            full = np.vstack(grids_temp[day])
            np.save(os.path.join(output_dir, f"grid_day_{day:03d}.npy"), full)

    return [[day] + global_results[day] for day in range(days)]