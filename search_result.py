class SearchResult:
    """Одна статья из результатов поиска: заголовок, идентификатор и фрагмент текста."""

    def __init__(self, title: str, page_id: int, snippet: str):
        if not title:
            raise ValueError("Заголовок статьи не может быть пустым.")
        if page_id <= 0:
            raise ValueError("Идентификатор статьи должен быть положительным числом.")

        self.__title = title
        self.__page_id = page_id
        self.__snippet = snippet

    @property
    def title(self) -> str:
        return self.__title

    @property
    def page_id(self) -> int:
        return self.__page_id

    @property
    def snippet(self) -> str:
        return self.__snippet