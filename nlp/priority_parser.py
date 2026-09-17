import re
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
            start = text.find(keyword)
            if start != -1:
                end = start + len(keyword)

                prefix = text_input[:start]
                if prefix.endswith(", "):
                    start -= 2

                text_input = text_input[:start] + text_input[end:]
                text_input = re.sub(r"\s+", " ", text_input).strip()
                return text_input, priority

    return text_input, "medium"