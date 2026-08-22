import time
from collections.abc import Callable
from datetime import datetime
from functools import wraps
from pathlib import Path
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def log(filename: str | Path | None = None) -> Callable[[Callable[P, R]], Callable[P, R]]:

    def write_log_choice(message: str) -> None:
        if filename:
            with open(filename, "a", encoding="utf-8") as f:
                f.write(f"{message}\n")
        else:
            print(f"{message}")

    def wrapper(func: Callable[P, R]) -> Callable[P, R]:

        @wraps(func)
        def inner(*args: P.args, **kwargs: P.kwargs) -> R:
            write_log_choice(f"{func.__name__} начала работу в {datetime.now()}")

            start_time = time.perf_counter()
            try:
                result = func(*args, **kwargs)
                write_log_choice(f"{func.__name__} ok")
                write_log_choice(f"Result of {func.__name__} work: {result}")
            except Exception as e:
                write_log_choice(f"{func.__name__} error: {e}. Inputs: {args}, {kwargs}")
                raise
            finally:
                execution_time = time.perf_counter() - start_time

                write_log_choice(
                    f"{func.__name__} с аргументами {args} и {kwargs} завершила работу в {datetime.now()}"
                )
                write_log_choice(f"Время выполнения: {execution_time:.6f} сек.")

            return result

        return inner

    return wrapper
