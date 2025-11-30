from datetime import datetime
from src.decorators import log
from tests.conftest import os, pytest, tempfile


class TestLogDecorator:
    """Тесты для декоратора log"""


def test_log_to_console_success(capsys):
    """Тест успешного выполнения функции с выводом в консоль"""

    @log()
    def multiply(a, b):
        return a * b

    result = multiply(4, 5)

    assert result == 20

    captured = capsys.readouterr()
    output = captured.out

    assert "Функция 'multiply' начала выполнение" in output
    assert "Функция 'multiply' успешно завершилась. Результат: 20" in output


def test_log_to_console_exception(capsys):
    """Тест обработки исключения с выводом в консоль"""

    @log()
    def divide(a, b):
        return a / b

    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

    captured = capsys.readouterr()
    output = captured.out

    assert "Функция 'divide' начала выполнение" in output
    assert "Функция 'divide' завершилась с ошибкой" in output
    assert "Тип ошибки: ZeroDivisionError" in output
    assert "Аргументы: args=(10, 0), kwargs={}" in output


def test_log_to_file_success():
    """Тест успешного выполнения функции с записью в файл"""
    # Создаем временный файл с бинарным режимом для избежания проблем с кодировкой
    with tempfile.NamedTemporaryFile(mode="wb", delete=False, suffix=".txt") as f:
        temp_filename = f.name

    try:

        @log(filename=temp_filename)
        def add(a, b):
            return a + b

        result = add(3, 7)
        assert result == 10

        # Читаем файл в бинарном режиме и декодируем с обработкой ошибок
        with open(temp_filename, "rb") as f:
            binary_content = f.read()

        # Пытаемся декодировать разными способами
        try:
            file_content = binary_content.decode("utf-8")
        except UnicodeDecodeError:
            try:
                file_content = binary_content.decode("cp1251")
            except UnicodeDecodeError:
                file_content = binary_content.decode("utf-8", errors="replace")

        assert "Функция 'add' начала выполнение" in file_content
        assert "Функция 'add' успешно завершилась. Результат: 10" in file_content

    finally:
        if os.path.exists(temp_filename):
            os.unlink(temp_filename)


def test_log_to_file_exception():
    """Тест обработки исключения с записью в файл"""
    with tempfile.NamedTemporaryFile(mode="wb", delete=False, suffix=".txt") as f:
        temp_filename = f.name

    try:

        @log(filename=temp_filename)
        def raise_value_error(a, b):
            raise ValueError("Custom error message")

        with pytest.raises(ValueError):
            raise_value_error(1, 2)

        # Читаем файл в бинарном режиме
        with open(temp_filename, "rb") as f:
            binary_content = f.read()

        # Декодируем с обработкой ошибок
        try:
            file_content = binary_content.decode("utf-8")
        except UnicodeDecodeError:
            try:
                file_content = binary_content.decode("cp1251")
            except UnicodeDecodeError:
                file_content = binary_content.decode("utf-8", errors="replace")

        assert "Функция 'raise_value_error' начала выполнение" in file_content
        assert "Функция 'raise_value_error' завершилась с ошибкой" in file_content
        assert "Тип ошибки: ValueError" in file_content
        assert "Сообщение: Custom error message" in file_content
        assert "Аргументы: args=(1, 2), kwargs={}" in file_content

    finally:
        if os.path.exists(temp_filename):
            os.unlink(temp_filename)


def test_log_preserves_function_metadata():
    """Тест сохранения метаданных оригинальной функции"""

    @log()
    def example_function(x: int, y: int) -> int:
        """Пример функции с документацией"""
        return x + y

    # Проверяем сохранение метаданных
    assert example_function.__name__ == "example_function"
    assert example_function.__doc__ == "Пример функции с документацией"
    assert hasattr(example_function, "__wrapped__")


def test_log_with_keyword_arguments(capsys):
    """Тест работы с именованными аргументами"""

    @log()
    def greet(name, greeting="Hello", punctuation="!"):
        return f"{greeting}, {name}{punctuation}"

    result = greet("Marina", greeting="Hi", punctuation="!!")
    assert result == "Hi, Marina!!"

    captured = capsys.readouterr()
    output = captured.out

    assert "Функция 'greet' начала выполнение" in output
    assert "Функция 'greet' успешно завершилась. Результат: Hi, Marina!!" in output


def test_log_custom_exception(capsys):
    """Тест обработки пользовательского исключения"""

    class CustomException(Exception):
        pass

    @log()
    def raise_custom_exception():
        raise CustomException("This is a custom exception")

    with pytest.raises(CustomException):
        raise_custom_exception()

    captured = capsys.readouterr()
    output = captured.out

    assert "Функция 'raise_custom_exception' начала выполнение" in output
    assert "Функция 'raise_custom_exception' завершилась с ошибкой" in output
    assert "Тип ошибки: CustomException" in output
