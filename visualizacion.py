import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import imageio
import os
import argparse
from tqdm import tqdm

def create_animation(args):
    # 0=White (S), 1=Red (I), 2=Green (R), 3=Black (D)
    cmap = mcolors.ListedColormap(['white', 'red', 'lightgreen', 'black'])
    bounds = [0, 1, 2, 3, 4]
    norm = mcolors.BoundaryNorm(bounds, cmap.N)

    frames = []
    
    if not os.path.exists(args.seq_dir) or not os.path.exists(args.par_dir):
        print("Missing output directories.")
        return

    seq_files = sorted([f for f in os.listdir(args.seq_dir) if f.startswith('grid_day_') and f.endswith('.npy')])
    par_files = sorted([f for f in os.listdir(args.par_dir) if f.startswith('grid_day_') and f.endswith('.npy')])
    
    num_days = min(len(seq_files), len(par_files))
    if num_days == 0:
        print("No grids found to visualize.")
        return

    days_to_vis = list(range(0, num_days, args.step))
    
    print(f"Generating visualization for {len(days_to_vis)} frames...")
    
    for day in tqdm(days_to_vis):
        grid_s = np.load(os.path.join(args.seq_dir, f"grid_day_{day:03d}.npy"))
        grid_p = np.load(os.path.join(args.par_dir, f"grid_day_{day:03d}.npy"))
        
        fig, axes = plt.subplots(1, 2, figsize=(10, 5))
        
        axes[0].imshow(grid_s, cmap=cmap, norm=norm, interpolation='nearest')
        axes[0].set_title(f"Secuencial - Día {day}")
        axes[0].axis('off')
        
        axes[1].imshow(grid_p, cmap=cmap, norm=norm, interpolation='nearest')
        axes[1].set_title(f"Paralelo - Día {day}")
        axes[1].axis('off')
        
        fig.tight_layout()
        
        # 🔥 FIX PARA WINDOWS (TkAgg)
        fig.canvas.draw()
        buf = np.asarray(fig.canvas.buffer_rgba())
        image = buf[:, :, :3]  # quitar canal alpha
        
        frames.append(image.copy())
        
        plt.close(fig)
        
    print(f"Saving to {args.output}...")

    try:
        imageio.mimsave(args.output, frames, fps=10)
    except Exception as e:
        print(f"Failed to save {args.output}: {e}")
        fallback = args.output.replace('.mp4', '.gif')
        print(f"Trying to save as {fallback} instead")
        imageio.mimsave(fallback, frames, fps=10)
        
    print("Done!")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--seq_dir', type=str, default='Secuencial/output')
    parser.add_argument('--par_dir', type=str, default='Paralelo/output')
    parser.add_argument('--output', type=str, default='comparacion.mp4')
    parser.add_argument('--step', type=int, default=5, help="Plot every N days")
    
    args = parser.parse_args()
    create_animation(args)