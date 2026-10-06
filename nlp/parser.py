from nlp.models import ParsedTask
from nlp.date_parser import parse_date
from nlp.time_parser import parse_time
from nlp.priority_parser import parse_priority

def parse_message(text: str):
    text, date = parse_date(text)
    text, time = parse_time(text)
    text, priority = parse_priority(text)
    title = text[0].upper() + text[1:]

    return ParsedTask(title=title, date=date, time=time, priority=priority)