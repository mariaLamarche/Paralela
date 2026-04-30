rom simulation import simulate
import pandas as pd
import time
import matplotlib.pyplot as plt
import os

# ==============================
# Preparar entorno
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
# Ejecución
# ==============================

if __name__ == '__main__':
    print("Iniciando simulación paralela...")

    start = time.time()

    results = simulate(
        365,
        1000,
        params,
        cores=4,
        save_grids=True,          
        output_dir=output_dir     
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
    df.to_csv(os.path.join(output_dir, "results.csv"), index=False)

    print("CSV guardado")

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
    plt.title("Modelo SIR - Paralelo")

    plt.legend()

    plt.savefig(os.path.join(output_dir, "sir_plot.png"))

    plt.show()
