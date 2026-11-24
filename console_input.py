import constants


class ConsoleInput:
    """Читает строки с консоли и проверяет их формат."""

    def read_line(self, prompt: str) -> str:
        """Читает строку без пробелов по краям. Пустую строку считает ошибкой."""
        text = input(prompt).strip()
        if not text:
            raise ValueError("Пустой ввод. Введите запрос или команду (/помощь — список команд).")
        return text

    def is_command(self, text: str) -> bool:
        """Проверяет, является ли строка командой (начинается с «/»)."""
        return text.startswith(constants.COMMAND_PREFIX)

    def parse_choice(self, text: str, results_count: int) -> int:
        """Превращает строку в номер статьи от 1 до results_count."""
        if not text.isdecimal():
            raise ValueError("Введите номер статьи цифрами.")

        number = int(text)
        if not 1 <= number <= results_count:
            raise ValueError(f"Номер должен быть от 1 до {results_count}.")
        return number