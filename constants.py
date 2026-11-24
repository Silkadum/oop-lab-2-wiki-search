"""Константы программы: адреса Википедии, параметры запроса и команды."""

# ----- Википедия -----

API_URL = "https://ru.wikipedia.org/w/api.php"
ARTICLE_URL = "https://ru.wikipedia.org/w/index.php?curid={page_id}"
USER_AGENT = "WikiSearchLab/1.0 (educational project)"
TIMEOUT_SECONDS = 10

# Регулярное выражение для HTML-тегов во фрагментах текста
HTML_TAG_PATTERN = r"<[^>]+>"

# ----- Консоль -----

COMMAND_PREFIX = "/"
EXIT_COMMAND = "/выход"
HELP_COMMAND = "/помощь"
BACK_COMMAND = "/назад"

# Максимальная длина фрагмента текста в списке результатов
SNIPPET_MAX_LENGTH = 150
