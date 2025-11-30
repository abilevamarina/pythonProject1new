import functools
from datetime import datetime


def log(temp_filename=None):  # Должен принимать параметр filename
    """
    Декоратор для логирования
    """

    def decorator(func):  # Внутренняя функция, принимающая декорируемую функцию
        @functools.wraps(func)
        def wrapper(*args, **kwargs):  # Функция-обёртка
            func_name = func.__name__
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Логируем начало выполнения
            start_message = f"[{timestamp}] Функция '{func_name}' начала выполнение"
            _log_message(start_message, temp_filename)

            try:
                # Выполняем оригинальную функцию
                result = func(*args, **kwargs)

                # Логируем успешное завершение
                success_message = f"[{timestamp}] Функция '{func_name}' успешно завершилась. Результат: {result}"
                _log_message(success_message, temp_filename)

                return result  # Возвращаем результат функции

            except Exception as e:
                # Логируем ошибку
                error_message = (
                    f"[{timestamp}] Функция '{func_name}' завершилась с ошибкой:\n"
                    f"  - Тип ошибки: {type(e).__name__}\n"
                    f"  - Сообщение: {str(e)}\n"
                    f"  - Аргументы: args={args}, kwargs={kwargs}"
                )
                _log_message(error_message, temp_filename)
                raise  # Пробрасываем исключение дальше

        return wrapper  # Возвращаем функцию-обёртку
    return decorator  # Возвращаем декоратор


def _log_message(message, temp_filename):
    """Вспомогательная функция"""
    if temp_filename:
        with open(temp_filename, 'a', encoding='utf-8') as f:
            f.write(message + '\n')
    else:
        print(message)
