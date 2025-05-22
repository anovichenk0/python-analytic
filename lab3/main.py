import time
import functools
from datetime import datetime
from threading import Lock
from typing import Any, Callable, TypeVar

F = TypeVar("F", bound=Callable)

def log_decorator(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = datetime.now()
        with open("log.txt", "a", encoding="utf-8") as f:
            f.write(f"[{start_time.strftime('%Y-%m-%d %H:%M:%S')}] "
                    f"Функция '{func.__name__}' вызвана с аргументами: {args}\n")

        t0 = time.time()
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            error_time = datetime.now()
            with open("log.txt", "a", encoding="utf-8") as f:
                f.write(f"[{error_time.strftime('%Y-%m-%d %H:%M:%S')}] "
                        f"Ошибка в функции '{func.__name__}': {str(e)}\n")
            raise
        else:
            t1 = time.time()
            end_time = datetime.now()
            duration = round(t1 - t0, 3)
            with open("log.txt", "a", encoding="utf-8") as f:
                f.write(f"[{end_time.strftime('%Y-%m-%d %H:%M:%S')}] "
                        f"Функция '{func.__name__}' завершена. Время выполнения: {duration} сек.\n")
            return result
    return wrapper


@log_decorator
def calculate(a: float, b: float, operation: str) -> float:
    match operation:
        case "+":
            return a + b
        case "-":
            return a - b
        case "*":
            return a * b
        case "/":
            return a / b
        case _:
            raise ValueError("Неподдерживаемая операция")


def rate_limit(max_calls: int, period: float) -> Callable[[Callable], Callable]:
    lock = Lock()

    def decorator(func: Callable) -> Callable:
        calls = []

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            with lock:
                nonlocal calls
                calls = [call for call in calls if now - call < period]
                if len(calls) < max_calls:
                    calls.append(now)
                    return func(*args, **kwargs)
                print("Превышен лимит вызовов. Попробуйте позже.")
        return wrapper
    return decorator


@rate_limit(max_calls=3, period=60)
def send_message(message: str) -> None:
    print(f"Сообщение отправлено: {message}")


def cache_decorator(func: Callable) -> Callable:
    cache = {}

    @functools.wraps(func)
    def wrapper(*args: Any) -> Any:
        if args in cache:
            return cache[args]
        result = func(*args)
        cache[args] = result
        return result
    return wrapper


@cache_decorator
def fibonacci(n: int) -> int:
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)



result = calculate(10, 5, "+")
print(f"Результат calculate(10, 5, '+'): {result}")

for i in range(5):
    print(f"Попытка отправки сообщения #{i+1}")
    send_message("Привет!")

print(f"Вызов fibonacci(10): {fibonacci(10)}")
print(f"Повторный вызов fibonacci(10): {fibonacci(10)}")
print(f"Вызов fibonacci(8): {fibonacci(8)}")
print(f"Повторный вызов fibonacci(8): {fibonacci(8)}")