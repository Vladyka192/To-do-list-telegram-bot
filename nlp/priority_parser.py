PRIORITY_KEYWORDS = {
    "high": [
        "срочно",
        "важно",
        "высокий приоритет",
        "критично",
        "очень важно",
    ],
    "medium": [
        "обычный приоритет",
        "средний приоритет",
    ],
    "low": [
        "не срочно",
        "низкий приоритет",
        "можно позже",
    ],
}

def parse_priority(text_input: str):
    text = text_input.lower()

    for priority, keywords in PRIORITY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                result = text.replace(keyword, "")
                return result, priority

    return text_input, "medium"