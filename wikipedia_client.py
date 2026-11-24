import requests

from wikipedia_error import WikipediaError


class WikipediaClient:
    """Отправляет поисковый запрос к API Википедии и возвращает ответ сервера в виде текста."""

    _API_URL = "https://ru.wikipedia.org/w/api.php"
    _USER_AGENT = "WikiSearchLab/1.0 (educational project)"
    _TIMEOUT_SECONDS = 10

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
                self._API_URL,
                params=params,
                headers={"User-Agent": self._USER_AGENT},
                timeout=self._TIMEOUT_SECONDS,
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