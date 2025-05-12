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
    
    for i in range(len(y_interp)):
        if y_interp[i] != y_interp[i]:
            valid_points = []
            for j in range(len(y_interp)):
                if y_interp[j] == y_interp[j]:
                    valid_points.append(j)
            
            closest = sorted(valid_points, key=lambda j: abs(x[j] - x[i]))[:3]
            closest = sorted(closest)
            
            if len(closest) >= 3:
                x0, x1, x2 = x[closest[0]], x[closest[1]], x[closest[2]]
                y0, y1, y2 = y_interp[closest[0]], y_interp[closest[1]], y_interp[closest[2]]
                
                #  Метод Крамера!
                det = (x0**2 * (x1 - x2)) + (x0 * (x2**2 - x1**2)) + (x1**2 * x2 - x2**2 * x1)
                det_a = y0 * (x1 - x2) + y1 * (x2 - x0) + y2 * (x0 - x1)
                det_b = x0**2 * (y1 - y2) + y0 * (x2**2 - x1**2) + x1**2 * y2 - x2**2 * y1
                det_c = x0**2 * (x1 * y2 - x2 * y1) + x0 * (x2**2 * y1 - x1**2 * y2) + y0 * (x1**2 * x2 - x2**2 * x1)
                
                a = det_a / det
                b = det_b / det
                c = det_c / det
                
                y_interp[i] = a * x[i]**2 + b * x[i] + c
                
                info = {
                    'x': x[i],
                    'used_points': [(x[closest[0]], y[closest[0]]), 
                                (x[closest[1]], y[closest[1]]), 
                                (x[closest[2]], y[closest[2]])],
                    'interpolated_value': y_interp[i],
                    'method': 'quadratic',
                    'coefficients': {'a': a, 'b': b, 'c': c}
                }
                interpolation_info[i] = info
                
                if verbose:
                    print(f"Точка x={x[i]}: использованы точки (x={x[closest[0]]}, y={y[closest[0]]}), "
                          f"(x={x[closest[1]]}, y={y[closest[1]]}), (x={x[closest[2]]}, y={y[closest[2]]})")
                    print(f"Коэффициенты: a={a:.4f}, b={b:.4f}, c={c:.4f}")
                    print(f"Результат интерполяции: {y_interp[i]:.2f}\n")
                
            elif len(closest) >= 2:
                # Линейная интерполяция, если не хватает точек
                left, right = closest[0], closest[-1]
                y_interp[i] = y_interp[left] + (y_interp[right] - y_interp[left]) * (x[i] - x[left]) / (x[right] - x[left])
                
                info = {
                    'x': x[i],
                    'used_points': [(x[left], y[left]), (x[right], y[right])],
                    'interpolated_value': y_interp[i],
                    'method': 'linear (fallback)'
                }
                interpolation_info[i] = info
                
                if verbose:
                    print(f"Точка x={x[i]}: недостаточно точек для квадратичной интерполяции")
                    print(f"Использована линейная интерполяция между (x={x[left]}, y={y[left]}) и (x={x[right]}, y={y[right]})")
                    print(f"Результат интерполяции: {y_interp[i]:.2f}\n")
    
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