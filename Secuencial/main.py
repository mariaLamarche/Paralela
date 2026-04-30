from simulation import simulate
import pandas as pd
import time
import matplotlib.pyplot as plt
import os

# ==============================
# Preparar ruta correcta
# ==============================

base_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(base_dir, "output")

os.makedirs(output_dir, exist_ok=True)

# ==============================
# Parámetros del modelo
# ==============================

params = {
    "beta": 0.3,
    "gamma": 0.1
}

# ==============================
# Ejecución de la simulación
# ==============================

start = time.time()

results = simulate(
    50,
    100,
    params,
    save_grids=True,          # 🔥 IMPORTANTE
    output_dir=output_dir     # 🔥 IMPORTANTE
)

end = time.time()

print("Tiempo:", end - start, "segundos")

# ==============================
# Mostrar resultados
# ==============================

for r in results:
    print(r)

# ==============================
# Guardar CSV
# ==============================

df = pd.DataFrame(results, columns=["day", "S", "I", "R"])

csv_path = os.path.join(output_dir, "results.csv")
df.to_csv(csv_path, index=False)

print(f"CSV guardado en {csv_path}")

# ==============================
# Gráfica
# ==============================

days = [r[0] for r in results]
S = [r[1] for r in results]
I = [r[2] for r in results]
R = [r[3] for r in results]

plt.figure()

plt.plot(days, S, label="Susceptibles")
plt.plot(days, I, label="Infectados")
plt.plot(days, R, label="Recuperados")

plt.xlabel("Días")
plt.ylabel("Población")
plt.title("Modelo SIR - Secuencial")

plt.legend()

img_path = os.path.join(output_dir, "sir_plot.png")
plt.savefig(img_path)

print(f"Gráfica guardada en {img_path}")

plt.show()
plt.close()
