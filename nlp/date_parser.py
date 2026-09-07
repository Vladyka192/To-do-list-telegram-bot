import dateparser
from dateparser.search import search_dates

# def parse_date(text_input: str, languages: list):
#     settings = {
#         'USE_GIVEN_LANGUAGE_ORDER': True,
#         'PREFER_DATES_FROM': 'future', 
#         'RETURN_AS_TIMEZONE_AWARE': True
#     }

#     return dateparser.parse(text_input, settings=settings, languages=languages)

date = search_dates("Завтра в 15:00 подготовить отчет", languages=['ru', 'en'])
print(date)