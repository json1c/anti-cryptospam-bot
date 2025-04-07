# tgbot/services/check_smart_spam.py
import math
import re

SUSPICIOUS_PHRASES = [
    "ставь +", "плюс в лс", "пишите в личные", "удаленная занятость", "+ в лс", "плюс мне", "пишите в личку",
    "финансовый поток", "удаленная занятость", "заработок от", "доход от",
    "ищем активных", "партнерство", "осталось мест", "финансовая независимость",
    "взаимовыгодных условиях", "приглашаем к сотрудничеству", "количество мест ограничено",
    "подробная информация в личку", "1-2 часа", "активных людей", "свободных мест", "удаленную деятельность", "в день"
]

EMOTIONAL_WORDS = ["срочно", "успей", "только сегодня", "уникальная возможность", "осталось"]


MAX_SCORE = 9

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def score_message(text: str) -> int:
    text = text.lower()
    score = 0

    for phrase in SUSPICIOUS_PHRASES:
        if phrase in text:
            score += 4

    money_matches = re.findall(r"\d+\s*(\$|usd|usdt|доллар|бакс)", text)
    score += len(money_matches) * 2

    for word in EMOTIONAL_WORDS:
        if word in text:
            score += 2

    if len(text.split()) < 10 and "пиши" in text:
        score += 3

    return score

def work_spam_probability(text: str) -> float:
    raw_score = score_message(text)
    normalized_score = raw_score / MAX_SCORE * 6 - 3
    probability = sigmoid(normalized_score)

    return round(probability * 100, 2)
