class SearchResult:
    """Одна статья из результатов поиска: заголовок, идентификатор и фрагмент текста."""

    def __init__(self, title: str, page_id: int, snippet: str):
        if not title:
            raise ValueError("Заголовок статьи не может быть пустым.")
        if page_id <= 0:
            raise ValueError("Идентификатор статьи должен быть положительным числом.")

        self._title = title
        self._page_id = page_id
        self._snippet = snippet

    @property
    def title(self) -> str:
        return self._title

    @property
    def page_id(self) -> int:
        return self._page_id

    @property
    def snippet(self) -> str:
        return self._snippet