

import re

def extract(row: str):

    pattern = re.compile(
        r'(?P<month>\w{3})\s'
        r'(?P<day>\d{1,2})\s'
        r'(?P<time>\d{2}:\d{2}:\d{2})\s.+:\s'
        r'(?P<message>.*)'
    )

    match = re.search(pattern, row)

    if match:
        return match.groupdict()

    return None
