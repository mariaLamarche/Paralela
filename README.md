# Simulación SIR - Modelo de Propagación Epidemiológica

Una implementación del modelo **SIR (Susceptible-Infected-Recovered)** en una grilla 2D para simular la propagación de enfermedades. El proyecto incluye versiones **secuencial** y **paralela** (usando multiprocessing) para análisis de rendimiento y escalabilidad.

## 📋 Descripción del Proyecto

Este proyecto simula la dinámica de propagación de una enfermedad infecciosa en una población espacialmente distribuida usando el modelo epidemiológico SIR. La simulación:

- **Modela tres estados**: Susceptibles (S), Infectados (I) y Recuperados (R)
- **Utiliza una grilla 2D** donde cada célula representa un individuo
- **Implementa dos variantes**:
  - Simulación secuencial
  - Simulación paralela con distribución de datos entre procesos
- **Genera visualizaciones** de la evolución temporal de la enfermedad

## 🏗️ Estructura del Proyecto

```
sir_simulation/
├── core/
│   └── model.py              # Núcleo del modelo SIR
├── Secuencial/
│   ├── main.py              # Script de ejecución secuencial
│   ├── simulation.py        # Implementación secuencial
│   └── output/              # Grillas guardadas (archivos .npy)
├── Paralelo/
│   ├── main.py              # Script de ejecución paralela
│   ├── simulation.py        # Implementación paralela con multiprocessing
│   └── output/              # Grillas guardadas (archivos .npy)
├── experimentos.py          # Script para análisis de escalabilidad
├── visualizacion.py         # Generación de visualizaciones
├── scaling_results.json     # Resultados de experimentos de rendimiento
├── requirements.txt         # Dependencias del proyecto
└── README.md               # Este archivo
```

## 🧬 Modelo SIR

El modelo SIR es un modelo epidemiológico clásico que divide la población en tres compartimentos:

- **S (Susceptible)**: Individuos sanos que pueden contraer la enfermedad
- **I (Infected)**: Individuos contagiados que pueden transmitir la enfermedad
- **R (Recovered)**: Individuos recuperados que desarrollaron inmunidad

### Parámetros

- **β (beta)**: Probabilidad de transmisión por contacto infectado
  - Rango típico: 0.0 - 1.0
  - Valor por defecto: 0.3

- **γ (gamma)**: Tasa de recuperación (inverso del período infeccioso)
  - Rango típico: 0.0 - 1.0
  - Valor por defecto: 0.1

### Dinámica

Cada iteración de simulación:
1. Se cuentan los infectados en la vecindad de 8 células (Moore neighborhood)
2. Las células susceptibles se infectan probabilísticamente
3. Las células infectadas se recuperan con probabilidad γ
4. Se almacenan estadísticas globales (S, I, R)

## 📦 Instalación

### Requisitos
- Python 3.6+
- pip o conda

### Instalación de dependencias

```bash
pip install -r requirements.txt
```

### Dependencias
- **numpy**: Computaciones numéricas y manejo de grillas
- **matplotlib**: Visualización de resultados
- **imageio**: Creación de animaciones
- **tqdm**: Barras de progreso en terminal

## 🚀 Uso

### Simulación Secuencial

```bash
cd Secuencial
python main.py
```

**Parámetros predeterminados**:
- Tamaño de grilla: 100x100
- Días simulados: 50
- β = 0.3, γ = 0.1

Genera archivos `.npy` en `Secuencial/output/` para cada día.

### Simulación Paralela

```bash
cd Paralelo
python main.py
```

**Parámetros predeterminados**:
- Tamaño de grilla: 1000x1000
- Días simulados: 365
- Cores: 4
- β = 0.3, γ = 0.1

Distribuye la grilla entre múltiples procesos con intercambio de ghost cells.

### Análisis de Escalabilidad

```bash
python experimentos.py
```

Ejecuta pruebas de rendimiento comparando:
- Simulación secuencial (baseline)
- Simulación paralela con 1, 2, 4 y 8 cores
- Calcula speedup para cada configuración
- Guarda resultados en `scaling_results.json`

### Visualización

```bash
python visualizacion.py
```

Genera visualizaciones y animaciones de los archivos `.npy` guardados.

## 📊 Estructura del Código

### `core/model.py`
Contiene la función central `update_grid()` que implementa la lógica del modelo SIR:
- Busca vecinos infectados en vecindad de 8 células
- Calcula probabilidades de infección
- Actualiza estados (S → I → R)

```python
def update_grid(grid, params):
    """
    Actualiza una iteración del modelo SIR
    
    Args:
        grid: Array 2D con estados [0=S, 1=I, 2=R]
        params: Dict con 'beta' y 'gamma'
    
    Returns:
        grid: Array actualizado
    """
```

### `Secuencial/simulation.py`
Implementación simple y directa:
- Procesa la grilla completa en cada iteración
- Fácil de entender y depurar
- Útil como baseline para comparación

### `Paralelo/simulation.py`
Implementación paralela usando multiprocessing:
- Divide la grilla horizontalmente entre procesos
- Utiliza pipes para intercambio de ghost cells (frontera)
- Usa Queue para recolectar resultados de todos los procesos
- Requiere sincronización entre procesos

## 🔧 Configuración Personalizada

Para ejecutar con parámetros personalizados, edita los archivos `main.py`:

### Secuencial
```python
results = simulate(
    days=100,           # Número de días
    size=200,           # Tamaño de grilla (NxN)
    params={
        "beta": 0.4,    # Tasa de transmisión
        "gamma": 0.15   # Tasa de recuperación
    },
    save_grids=True,    # Guardar snapshots
    output_dir="output"
)
```

### Paralelo
```python
results = simulate(
    days=100,
    size=200,
    params={
        "beta": 0.4,
        "gamma": 0.15
    },
    cores=4,            # Número de procesos
    save_grids=True,
    output_dir="output"
)
```

## 📈 Resultados y Análisis

### Archivos de Salida

- **`grid_day_XXX.npy`**: Snapshots de la grilla para cada día (formato NumPy)
- **`scaling_results.json`**: Resultados de análisis de escalabilidad con tiempos y speedups

### Interpretación de Resultados

```json
{
    "sequential": 45.23,
    "parallel": {
        "1": {"time": 45.10, "speedup": 1.00},
        "2": {"time": 24.50, "speedup": 1.85},
        "4": {"time": 13.20, "speedup": 3.43},
        "8": {"time": 8.50, "speedup": 5.33}
    }
}
```

**Observaciones comunes**:
- El speedup generalmente es sublineal debido a overhead de comunicación
- La versión paralela se beneficia más con grillas grandes (1000x1000+)
- Ghost cell exchange es el cuello de botella principal

## 🎨 Visualizaciones

Las animaciones muestran:
- **Progresión color**: Azul (susceptibles) → Rojo (infectados) → Verde (recuperados)
- **Evolución temporal**: Cómo la enfermedad se propaga y controla
- **Estadísticas**: Gráficas de S, I, R en el tiempo

## ⚡ Consideraciones de Rendimiento

### Factores que afectan la velocidad

1. **Tamaño de grilla**: O(N²) complejidad espacial
2. **Número de días**: O(T) complejidad temporal
3. **Comunicación inter-proceso**: Overhead en versión paralela
4. **Cache locality**: Acceso a memoria contigua

### Recomendaciones

- Para grillas < 500x500: usar versión secuencial
- Para grillas > 500x500: considerar paralela con 4-8 cores
- Monitorear el overhead: `ghost cell exchange`

## 🐛 Debugging y Troubleshooting

### Problema: ImportError en simulación paralela
**Solución**: Asegúrate de ejecutar desde el directorio raíz:
```bash
cd ..
python Paralelo/main.py
```

### Problema: Bajo speedup en versión paralela
**Posibles causas**:
- Grilla muy pequeña (overhead > cálculo)
- Demasiados procesos (más sincronización)
- I/O disk está limitando (guardar grillas)

**Soluciones**:
- Aumentar tamaño de grilla
- Reducir número de cores
- Desactivar `save_grids` durante benchmarks

### Problema: Memoria insuficiente
**Soluciones**:
- Reducir tamaño de grilla
- Reducir número de días
- Desactivar guardado de grillas

## 📚 Referencias

- Keeling, M. J., & Rohani, P. (2008). **Modeling Infectious Diseases**. Princeton University Press.
- Kermack-McKendrick SIR Model: https://en.wikipedia.org/wiki/Compartmental_models_in_epidemiology

## 📄 Licencia

Este proyecto es de código abierto y disponible para uso educativo y de investigación.

## 👤 Autor

Proyecto de simulación epidemiológica con enfoque en análisis de escalabilidad paralela.

---

**Última actualización**: Abril 2026
