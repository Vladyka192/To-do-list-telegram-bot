import re
from datetime import time

TIME_PATTERN = re.compile(
    r"(?P<time>(?:[01]\d|2[0-3]):[0-5]\d)"
)

def parse_time(text_input: str):
    match = TIME_PATTERN.search(text_input)

    if not match:
        return text_input, None

    time_str = match.group('time')

    hour, minute = map(int, time_str.split(":"))
    parsed_time = time(hour=hour, minute=minute)

    # Начало и конец найденного времени
    start = match.start()
    end = match.end()

    # Проверяем, есть ли непосредственно перед временем "в "
    prefix = text_input[:start]

    if prefix.lower().endswith("в "):
        start -= 3

    # Удаляем только найденный участок
    text_input = text_input[:start] + text_input[end:]

    # Убираем лишние пробелы
    text_input = re.sub(r"\s+", " ", text_input).strip()

    return text_input, parsed_time