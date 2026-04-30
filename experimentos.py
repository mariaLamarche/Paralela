import subprocess
import time
import json
import os

def run_experiments():
    cores_list = [1, 2, 4, 8]
    results = {}

    rows = 1000
    cols = 1000
    days = 365

    print(f"Starting Strong Scaling Experiments for {rows}x{cols} grid over {days} days...")
    
    # Run sequential as baseline
    print("Running sequential benchmark...")
    start = time.time()
    subprocess.run(["python", "secuencial/main.py", "--rows", str(rows), "--cols", str(cols), "--days", str(days), "--save_grids"])
    seq_time = time.time() - start
    print(f"Sequential took: {seq_time:.2f}s")
    results['sequential'] = seq_time
    
    # Run parallel
    results['parallel'] = {}
    for cores in cores_list:
        print(f"Running parallel with {cores} cores...")
        start = time.time()
        # Save grids only for the 4 cores to use it for comparison later in animation
        save_flag = ["--save_grids"] if cores == 4 else []
        cmd = ["python", "paralelo/main.py", "--rows", str(rows), "--cols", str(cols), "--days", str(days), "--cores", str(cores)] + save_flag + ["--output_dir", f"output_paralelo_{cores}c"]
        subprocess.run(cmd)
        t = time.time() - start
        speedup = seq_time / t
        print(f"Cores: {cores}, Time: {t:.2f}s, Speedup: {speedup:.2f}x")
        results['parallel'][cores] = {
            'time': t,
            'speedup': speedup
        }

    # Save to file
    with open("scaling_results.json", "w") as f:
        json.dump(results, f, indent=4)
        
    print("Experiments completed. Results strictly saved to scaling_results.json")

if __name__ == '__main__':
    run_experiments()
