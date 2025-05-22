import os
from pathlib import Path
import numpy as np

def load_data(file_path: str, mode: str = 'np') -> np.ndarray:
    if mode == 'open':
        with open(file_path, 'r') as file:
            raw_values = [float(line.strip()) for line in file if line.strip()]
        return np.array(raw_values)
    else:
        return np.loadtxt(file_path)

def compute_stats(data: np.ndarray) -> dict:
    return {
        "average": float(np.mean(data)),
        "highest": float(np.max(data)),
        "lowest": float(np.min(data))
    }

def get_derivative(x_values: np.ndarray, y_values: np.ndarray) -> np.ndarray:
    return np.gradient(y_values, x_values)

def calculate_area(x_values: np.ndarray, y_values: np.ndarray) -> float:
    step = np.diff(x_values)
    mid_points = (y_values[:-1] + y_values[1:]) / 2
    return float(np.sum(mid_points * step))

def write_output(
    output_file: str,
    source_file: str,
    stats: dict,
    derivative_values: np.ndarray,
    total_area: float
) -> None:
    with open(output_file, 'w', encoding="utf-8") as file:
        file.write(f"Файл данных: {source_file}\n")
        file.write(f"Среднее значение: {stats['average']:.4f}\n")
        file.write(f"Максимум: {stats['highest']:.4f}\n")
        file.write(f"Минимум: {stats['lowest']:.4f}\n")
        file.write("Производная:\n")
        file.write(", ".join(f"{value:.4f}" for value in derivative_values) + "\n")
        file.write(f"Интеграл: {total_area:.4f}\n")
        
data_dir = Path(__file__).parent / 'data'
x_path = data_dir / 'xc.dat'

x = load_data(x_path)

for fname in sorted(os.listdir(data_dir)):
    if fname.startswith("yc-") and fname.endswith(".dat"):
        y_path = os.path.join(data_dir, fname)
        y = load_data(y_path)

        stats = compute_stats(y)
        deriv = get_derivative(x, y)
        integral = calculate_area(x, y)

        out_name = f"out_{fname}"
        out_path = os.path.join(data_dir, out_name)
        write_output(out_path, fname, stats, deriv, integral)