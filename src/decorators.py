import functools
from datetime import datetime


def log(filename=None):
    """
    Декоратор для логирования начала и конца выполнения функции,
    а также результатов или ошибок.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Формируем информацию о вызове функции
            func_name = func.__name__
            timestamp = datetime.now().strftime("Y-m-d H:M:S")

            # Логируем начало выполнения
            start_message = f"[{timestamp}] Функция '{func_name}' начала выполнение"
            log_message(start_message, filename)

            try:
                # Выполняем функцию
                result = func(*args, **kwargs)

                # Логируем успешное завершение
                success_message = f"[{timestamp}] Функция '{func_name}' успешно завершилась. Результат: {result}"
                log_message(success_message, filename)

                return result

            except Exception as e:
                # Логируем ошибку
                error_message = (
                    f"[{timestamp}] Функция '{func_name}' завершилась с ошибкой:\n"
                    f"  - Тип ошибки: {type(e).__name__}\n"
                    f"  - Сообщение: {str(e)}\n"
                    f"  - Аргументы: args={args}, kwargs={kwargs}"
                )
                log_message(error_message, filename)

                # Пробрасываем исключение дальше
                raise

        return wrapper

    return decorator


def log_message(message, filename):
    """Вспомогательная функция для записи лога в файл или консоль"""
    if filename:
        # Записываем в файл
        with open(filename, "a") as f:
            f.write(message + "\n")
    else:
        # Выводим в консоль
        print(message)
