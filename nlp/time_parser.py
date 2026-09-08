import re

def parse_time(text_input: str):
    pattern = r"(?P<time>([0-1][0-9]|[2]?[0-3]):[0-5][0-9])"
    match = re.search(pattern, text_input)

    time = match.group('time')
    if match:
        result = text_input.replace(time, "")
        return result, time

    return text_input, None
