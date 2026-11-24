import requests

import constants
from wikipedia_error import WikipediaError


class WikipediaClient:
    """Отправляет поисковый запрос к API Википедии и возвращает ответ сервера в виде текста."""

    def search(self, query: str) -> str:
        """Выполняет поиск и возвращает JSON-ответ сервера как строку."""
        params = {
            "action": "query",
            "list": "search",
            "format": "json",
            "utf8": 1,
            "srsearch": query,
        }

        try:
            response = requests.get(
                constants.API_URL,
                params=params,
                headers={"User-Agent": constants.USER_AGENT},
                timeout=constants.TIMEOUT_SECONDS,
            )
            response.raise_for_status()
        except requests.Timeout:
            raise WikipediaError("Сервер Википедии не ответил вовремя. Попробуйте ещё раз.") from None
        except requests.ConnectionError:
            raise WikipediaError("Не удалось подключиться к Википедии. Проверьте интернет.") from None
        except requests.HTTPError:
            raise WikipediaError(f"Сервер Википедии вернул ошибку {response.status_code}.") from None
        except requests.RequestException:
            raise WikipediaError("Ошибка при обращении к Википедии.") from None

        return response.text