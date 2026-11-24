from response_parser import ResponseParser
from wikipedia_client import WikipediaClient
from app import SearchApp
from browser_opener import BrowserOpener
from console_input import ConsoleInput
from console_output import ConsoleOutput


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