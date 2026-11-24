from api.response_parser import ResponseParser
from api.wikipedia_client import WikipediaClient
from app import SearchApp
from browser_opener import BrowserOpener
from ui.console_input import ConsoleInput
from ui.console_output import ConsoleOutput


def main() -> None:
    app = SearchApp(
        ConsoleInput(),
        ConsoleOutput(),
        WikipediaClient(),
        ResponseParser(),
        BrowserOpener(),
    )
    app.run()


if __name__ == "__main__":
    main()