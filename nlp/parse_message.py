import re

message_entry = "Пойти в школу в 1:00"

pattern = r"(?P<time>([0-1][0-9]|[2]?[0-3]):[0-5][0-9])"

match = re.search(pattern, message_entry)

time = match.group('time')

if match:
    print(match.group('time'))
