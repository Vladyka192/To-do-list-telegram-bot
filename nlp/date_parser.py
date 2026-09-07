import dateparser

def parse_date(text_input: str, languages: list):
    settings = {
        'USE_GIVEN_LANGUAGE_ORDER': True,
        'PREFER_DATES_FROM': 'future', 
        'RETURN_AS_TIMEZONE_AWARE': True
    }

    return dateparser.parse(text_input, settings=settings, languages=languages)

date = parse_date("Завтра в 15:00 в школу", languages=['ru', 'en'])
