import html
import json
import re

from api.wikipedia_error import WikipediaError
from models.search_result import SearchResult


class ResponseParser:
    """Превращает JSON-ответ API Википедии в список результатов поиска."""

    _TAG_PATTERN = re.compile(r"<[^>]+>")

    def parse(self, response_text: str) -> list[SearchResult]:
        """Разбирает ответ сервера. Пустой список означает, что ничего не найдено."""
        try:
            data = json.loads(response_text)
        except json.JSONDecodeError:
            raise WikipediaError("Сервер вернул ответ в неожиданном формате.") from None

        if not isinstance(data, dict):
            raise WikipediaError("Сервер вернул ответ в неожиданном формате.")

        if "error" in data:
            info = data["error"].get("info", "неизвестная ошибка")
            raise WikipediaError(f"Википедия вернула ошибку: {info}")

        try:
            items = data["query"]["search"]
        except (KeyError, TypeError):
            raise WikipediaError("В ответе сервера нет результатов поиска.") from None

        results = []
        for item in items:
            try:
                snippet = self._clean_snippet(item.get("snippet", ""))
                results.append(SearchResult(item["title"], item["pageid"], snippet))
            except (KeyError, TypeError, ValueError):
                # Повреждённую запись пропускаем, остальные результаты показываем
                continue

        return results

    def _clean_snippet(self, snippet: str) -> str:
        """Убирает из фрагмента HTML-теги и превращает спецсимволы (&quot; и т.п.) в обычные."""
        without_tags = self._TAG_PATTERN.sub("", snippet)
        return html.unescape(without_tags).strip()