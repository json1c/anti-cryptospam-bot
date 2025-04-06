import re
from difflib import SequenceMatcher


def difflib_similarity(s1, s2):
    return SequenceMatcher(None, s1, s2).ratio() * 100

SPAM_KEYWORDS = [
    [r"^usd[тt]", "usdt"],
    [r"^[рp][aа]зд[aа]ч[aа]", "раздача"],
    [r"^[aа][kк][tт]и[bв][aа]ций", "активаций"],
    [r"^п[уy]л", "пул"],
    [r"^ч[eе][kк]", "чек"],
    [r"^[тt][оo]n", "ton"],
    [r"\$[тt]ru[mм][pр]", "$trump"]
]

def check_text(text: str):
    text = text.lower()

    for word in text.split():
        for regexp, keyword in SPAM_KEYWORDS:
            if match := re.search(regexp, word):
                found_word = match.group(0)
                confident = difflib_similarity(keyword, found_word)

                return found_word, keyword, confident
