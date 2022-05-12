from datetime import datetime


def convert_date(date_str: str):
    '''

    :param date_str: YYYY-MM-DD
    '''

    converted_date = datetime.strptime(date_str, '%Y-%m-%d').strftime('%Y-%m-%dT%H:%M:%SZ')
    return converted_date



