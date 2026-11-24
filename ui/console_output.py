from models.search_result import SearchResult


class ConsoleOutput:
    """Печатает в консоль результаты поиска и сообщения для пользователя."""

    _SNIPPET_MAX_LENGTH = 150

    def show_welcome(self) -> None:
        print("Поиск по русской Википедии.")
        print("Введите запрос или команду. Список команд: /помощь")

    def show_help(self) -> None:
        print("Команды:")
        print("  /помощь — показать этот список")
        print("  /назад  — вернуться к новому поиску (при выборе статьи)")
        print("  /выход  — завершить программу")

    def show_results(self, results: list[SearchResult]) -> None:
        if not results:
            print("По вашему запросу ничего не найдено.")
            return

        print(f"Найдено статей: {len(results)}")
        for number, result in enumerate(results, start=1):
            print(f"{number}. {result.title}")
            if result.snippet:
                print(f"   {self._shorten(result.snippet)}")

    def show_message(self, message: str) -> None:
        print(message)

    def show_error(self, message: str) -> None:
        print(f"Ошибка: {message}")

    def _shorten(self, text: str) -> str:
        """Обрезает длинный фрагмент, чтобы список оставался читаемым."""
        if len(text) <= self._SNIPPET_MAX_LENGTH:
            return text
        return text[: self._SNIPPET_MAX_LENGTH].rstrip() + "…"