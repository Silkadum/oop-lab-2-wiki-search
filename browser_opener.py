import webbrowser

import constants


class BrowserOpener:
    """Формирует ссылку на статью Википедии по её идентификатору и открывает её в браузере."""

    def article_url(self, page_id: int) -> str:
        """Возвращает ссылку на статью по её pageid."""
        return constants.ARTICLE_URL.format(page_id=page_id)

    def open_article(self, page_id: int) -> bool:
        """Открывает статью в браузере. Возвращает False, если браузер открыть не удалось."""
        try:
            return webbrowser.open(self.article_url(page_id))
        except webbrowser.Error:
            return False