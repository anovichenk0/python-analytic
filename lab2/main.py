import os
import json
import matplotlib.pyplot as plt

def read_data(filename):
    x = []
    y = []
    with open(filename, 'r') as f:
        next(f)  # Пропускаем заголовок
        for line in f:
            parts = line.strip().split(';')
            x.append(int(parts[0]))
            try:
                y.append(float(parts[1]))
            except ValueError:
                y.append(float('nan'))
    return x, y

def find_nearest_valid_indices(data, index):
    left = index - 1
    while left >= 0 and data[left] != data[left]:
        left -= 1
    
    right = index + 1
    while right < len(data) and data[right] != data[right]:
        right += 1
    
    return left, right

def linear_interpolation(x, y, verbose=False):
    y_interp = y.copy()
    interpolation_info = {}
    
    for i in range(len(y_interp)):
        if y_interp[i] != y_interp[i]:
            left, right = find_nearest_valid_indices(y_interp, i)
            
            if left >= 0 and right < len(y_interp):
                y_interp[i] = y_interp[left] + (y_interp[right] - y_interp[left]) * (x[i] - x[left]) / (x[right] - x[left])
                
                info = {
                    'x': x[i],
                    'used_points': [(x[left], y[left]), (x[right], y[right])],
                    'interpolated_value': y_interp[i],
                    'method': 'linear'
                }
                interpolation_info[i] = info
                
                if verbose:
                    print(f"Точка x={x[i]}: использованы точки (x={x[left]}, y={y[left]}) и (x={x[right]}, y={y[right]})")
                    print(f"Результат интерполяции: {y_interp[i]:.2f}\n")
    
    return y_interp, interpolation_info

def quadratic_interpolation(x, y, verbose=False):
    y_interp = y.copy()
    interpolation_info = {}

    # Получаем индексы всех известных (не NaN) точек
    valid_indices = [i for i in range(len(y)) if y[i] == y[i]]

    for i in range(len(y_interp)):
        if y_interp[i] != y_interp[i]:  # Если NaN
            left_points = sorted(
                [(j, abs(x[j] - x[i])) for j in valid_indices if x[j] < x[i]],
                key=lambda p: p[1]
            )
            right_points = sorted(
                [(j, abs(x[j] - x[i])) for j in valid_indices if x[j] > x[i]],
                key=lambda p: p[1]
            )

            left_candidates = [j for j, _ in left_points[:2]]
            right_candidates = [j for j, _ in right_points[:2]]

            candidates = []
            candidates.extend(left_candidates)
            candidates.extend(right_candidates)

            while len(candidates) < 3 and (left_points or right_points):
                if left_points:
                    extra = left_points.pop(0)[0]
                    if extra not in candidates:
                        candidates.append(extra)
                elif right_points:
                    extra = right_points.pop(0)[0]
                    if extra not in candidates:
                        candidates.append(extra)

            if len(candidates) < 3:
                continue

            unique_x = set(x[j] for j in candidates[:3])
            if len(unique_x) < 2:
                continue

            points = [(x[j], y_interp[j]) for j in candidates[:3]]
            x0, y0 = points[0]
            x1, y1 = points[1]
            x2, y2 = points[2]

            det = (x0**2 * (x1 - x2)) + (x0 * (x2**2 - x1**2)) + (x1**2 * x2 - x2**2 * x1)
            if det == 0:
                continue

            det_a = y0 * (x1 - x2) + y1 * (x2 - x0) + y2 * (x0 - x1)
            det_b = x0**2 * (y1 - y2) + y0 * (x2**2 - x1**2) + x1**2 * y2 - x2**2 * y1
            det_c = x0**2 * (x1 * y2 - x2 * y1) + x0 * (x2**2 * y1 - x1**2 * y2) + y0 * (x1**2 * x2 - x2**2 * x1)

            a = det_a / det
            b = det_b / det
            c = det_c / det

            interpolated = a * x[i]**2 + b * x[i] + c
            y_interp[i] = interpolated

            info = {
                'x': x[i],
                'used_points': points,
                'interpolated_value': interpolated,
                'method': 'quadratic',
                'coefficients': {'a': a, 'b': b, 'c': c}
            }
            interpolation_info[i] = info

            if verbose:
                print(f"Точка x={x[i]}: использованы точки:")
                for pt in points:
                    print(f"  (x={pt[0]}, y={pt[1]:.2f})")
                print(f"Коэффициенты: a={a:.4f}, b={b:.4f}, c={c:.4f}")
                print(f"Результат интерполяции: {interpolated:.2f}\n")

    return y_interp, interpolation_info

def save_results(filename, data):
    """Сохранение результатов в JSON файл"""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_file = os.path.join(script_dir, 'main.csv')
    
    try:
        # Чтение данных
        x, y = read_data(data_file)
        
        print("="*50)
        print("Линейная интерполяция:")
        print("="*50)
        y_linear, linear_info = linear_interpolation(x, y, verbose=True)
        
        print("\n" + "="*50)
        print("Квадратичная интерполяция:")
        print("="*50)
        y_quad, quad_info = quadratic_interpolation(x, y, verbose=True)
        
        results = {
            'linear_interpolation': {
                'values': list(zip(x, y_linear)),
                'details': linear_info
            },
            'quadratic_interpolation': {
                'values': list(zip(x, y_quad)),
                'details': quad_info
            }
        }
        
        output_json = os.path.join(script_dir, 'interpolation_results.json')
        save_results(output_json, results)
        print(f"\nРезультаты сохранены в файл: {output_json}")
        
        # Построение графиков
        plt.figure(figsize=(12, 6))
        plt.scatter(x, y, color='red', label='Исходные данные', zorder=3)
        plt.plot(x, y_linear, 'b--', label='Линейная интерполяция', alpha=0.7)
        plt.plot(x, y_quad, 'g-.', label='Квадратичная интерполяция', alpha=0.7)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('Интерполяция таблично заданной функции')
        plt.legend()
        plt.grid(True)
        
        output_img = os.path.join(script_dir, 'interpolation_plot.png')
        plt.savefig(output_img, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"График сохранён в файл: {output_img}")
    
    except FileNotFoundError:
        print(f"Ошибка: Файл {data_file} не найден!")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()