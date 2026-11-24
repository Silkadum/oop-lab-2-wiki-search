from api.response_parser import ResponseParser
from api.wikipedia_client import WikipediaClient
from api.wikipedia_error import WikipediaError
from browser_opener import BrowserOpener
from models.search_result import SearchResult
from ui.console_input import ConsoleInput
from ui.console_output import ConsoleOutput


class SearchApp:
    """Управляет работой программы: поиск, выбор статьи, команды и обработка ошибок."""

    _EXIT_COMMAND = "/выход"
    _HELP_COMMAND = "/помощь"
    _BACK_COMMAND = "/назад"

    def __init__(
        self,
        console_input: ConsoleInput,
        console_output: ConsoleOutput,
        client: WikipediaClient,
        parser: ResponseParser,
        browser: BrowserOpener,
    ):
        self._input = console_input
        self._output = console_output
        self._client = client
        self._parser = parser
        self._browser = browser
        self._running = False

    def run(self) -> None:
        """Запускает основной цикл программы."""
        self._output.show_welcome()
        self._running = True

        try:
            while self._running:
                self._search_step()
        except (KeyboardInterrupt, EOFError):
            # Ctrl+C или Ctrl+D: завершаем работу без трассировки
            self._output.show_message("")

        self._output.show_message("Работа завершена.")

    def _search_step(self) -> None:
        """Один цикл поиска: запрос, обращение к API, вывод и выбор статьи."""
        text = self._read("\nПоиск: ")
        if text is None:
            return

        if self._input.is_command(text):
            self._handle_command(text)
            return

        try:
            response_text = self._client.search(text)
            results = self._parser.parse(response_text)
        except WikipediaError as error:
            self._output.show_error(str(error))
            return

        self._output.show_results(results)
        if results:
            self._choice_step(results)

    def _choice_step(self, results: list[SearchResult]) -> None:
        """Просит выбрать статью, пока пользователь не введёт корректный номер или /назад."""
        while self._running:
            text = self._read(f"Номер статьи (1–{len(results)}) или /назад: ")
            if text is None:
                continue

            if self._input.is_command(text):
                if text.lower() == self._BACK_COMMAND:
                    return
                self._handle_command(text)
                continue

            try:
                number = self._input.parse_choice(text, len(results))
            except ValueError as error:
                self._output.show_error(str(error))
                continue

            self._open_article(results[number - 1])
            return

    def _open_article(self, result: SearchResult) -> None:
        """Печатает ссылку на статью и пытается открыть её в браузере."""
        url = self._browser.article_url(result.page_id)
        self._output.show_message(f"Открываю «{result.title}»: {url}")

        if not self._browser.open_article(result.page_id):
            self._output.show_error("Не удалось открыть браузер. Откройте ссылку вручную.")

    def _handle_command(self, text: str) -> None:
        """Выполняет команду, введённую пользователем."""
        command = text.lower()

        if command == self._EXIT_COMMAND:
            self._running = False
        elif command == self._HELP_COMMAND:
            self._output.show_help()
        elif command == self._BACK_COMMAND:
            self._output.show_error("Команда /назад работает только при выборе статьи.")
        else:
            self._output.show_error("Неизвестная команда. Список команд: /помощь")

    def _read(self, prompt: str) -> str | None:
        """Читает строку. При пустом вводе показывает ошибку и возвращает None."""
        try:
            return self._input.read_line(prompt)
        except ValueError as error:
            self._output.show_error(str(error))
            return None