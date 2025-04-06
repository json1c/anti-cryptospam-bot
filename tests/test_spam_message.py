import pytest

from tgbot.services.check_message import check_text


@pytest.mark.parametrize(
    "input_text, expected_keyword",
    [
        ("Раздача крипты", "раздача"),
        ("usdт подарок", "usdt"),
        ("чекнуть баланс", "чек"),
        ("TON в подарок", "ton"),
        ("пул раздачи", "пул"),
        ("$trump to the moon", "$trump"),
    ],
)
def test_check_text_detects_spam(input_text, expected_keyword):
    result = check_text(input_text)
    assert result is not None, f"Expected a keyword to be detected for the text: {input_text}"
    found_word, keyword, confident = result

    assert keyword == expected_keyword, f"Expected keyword {expected_keyword}, but got {keyword}"


def test_check_text_returns_none_for_clean_text():
    clean_text = "Обычное сообщение без спама"
    result = check_text(clean_text)
    assert result is None, "Expected clean text not to be classified as spam"
