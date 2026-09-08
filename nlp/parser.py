from datetime import datetime
# from models import ParsedTask
from date_parser import parse_date
from time_parser import parse_time
from priority_parser import parse_priority

def parse_message(text: str):
    text, date = parse_date(text)
    text, time = parse_time(text)
    text, priority = parse_priority(text)
    title = text

    print(date.date(), datetime.strptime(time, "%H:%M").time(), priority, title)

    # return ParsedTask(title=title, date=date, time=time, priority=priority)

parse_message("Завтра купить хлеб в 15:00, СРОЧНО")