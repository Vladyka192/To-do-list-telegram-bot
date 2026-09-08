from dateparser.search import search_dates

def parse_date(text_input: str):
    settings = {
        'USE_GIVEN_LANGUAGE_ORDER': True,
        'PREFER_DATES_FROM': 'future'
    }
    date = search_dates(text_input, settings=settings, languages=['ru', 'en'])
    result = text_input.replace(date[0][0], "")

    return result, date[0][1]