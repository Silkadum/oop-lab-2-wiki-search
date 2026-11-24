import constants
from response_parser import ResponseParser
from wikipedia_client import WikipediaClient
from wikipedia_error import WikipediaError
from browser_opener import BrowserOpener
from search_result import SearchResult
from console_input import ConsoleInput
from console_output import ConsoleOutput


class SearchApp:
    """Управляет работой программы: поиск, выбор статьи, команды и обработка ошибок."""

    def __init__(
        self,
        console_input: ConsoleInput,
        console_output: ConsoleOutput,
        client: WikipediaClient,
        parser: ResponseParser,
        browser: BrowserOpener,
    ):
        self.__input = console_input
        self.__output = console_output
        self.__client = client
        self.__parser = parser
        self.__browser = browser
        self.__running = False

    def run(self) -> None:
        """Запускает основной цикл программы."""
        self.__output.show_welcome()
        self.__running = True

        try:
            while self.__running:
                self._search_step()
        except (KeyboardInterrupt, EOFError):
            # Ctrl+C или Ctrl+D: завершаем работу без трассировки
            self.__output.show_message("")

        self.__output.show_message("Работа завершена.")

    def _search_step(self) -> None:
        """Один цикл поиска: запрос, обращение к API, вывод и выбор статьи."""
        text = self._read("\nПоиск: ")
        if text is None:
            return

        if self.__input.is_command(text):
            self._handle_command(text)
            return

        try:
            response_text = self.__client.search(text)
            results = self.__parser.parse(response_text)
        except WikipediaError as error:
            self.__output.show_error(str(error))
            return

        self.__output.show_results(results)
        if results:
            self._choice_step(results)

    def _choice_step(self, results: list[SearchResult]) -> None:
        """Просит выбрать статью, пока пользователь не введёт корректный номер или /назад."""
        while self.__running:
            text = self._read(f"Номер статьи (1–{len(results)}) или /назад: ")
            if text is None:
                continue

            if self.__input.is_command(text):
                if text.lower() == constants.BACK_COMMAND:
                    return
                self._handle_command(text)
                continue

            try:
                number = self.__input.parse_choice(text, len(results))
            except ValueError as error:
                self.__output.show_error(str(error))
                continue

            self._open_article(results[number - 1])
            return

    def _open_article(self, result: SearchResult) -> None:
        """Печатает ссылку на статью и пытается открыть её в браузере."""
        url = self.__browser.article_url(result.page_id)
        self.__output.show_message(f"Открываю «{result.title}»: {url}")

        if not self.__browser.open_article(result.page_id):
            self.__output.show_error("Не удалось открыть браузер. Откройте ссылку вручную.")

    def _handle_command(self, text: str) -> None:
        """Выполняет команду, введённую пользователем."""
        command = text.lower()

        match command:
            case constants.EXIT_COMMAND:
                self.__running = False
            case constants.HELP_COMMAND:
                self.__output.show_help()
            case constants.BACK_COMMAND:
                self.__output.show_error("Команда /назад работает только при выборе статьи.")
            case _:
                self.__output.show_error("Неизвестная команда. Список команд: /помощь")

    def _read(self, prompt: str) -> str | None:
        """Читает строку. При пустом вводе показывает ошибку и возвращает None."""
        try:
            return self.__input.read_line(prompt)
        except ValueError as error:
            self.__output.show_error(str(error))
            return None