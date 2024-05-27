import re
from typing import Tuple

# create array with all names of months
month_names = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]


def get_date_patterns() -> Tuple[str, str, str]:
    """Return strings containing regex pattern for year, month, day
    arguments:
        None
    return:
        year, month, day (tuple): Containing regular expression patterns for each field
    """

    # Regex to capture days, months and years with numbers
    # year should accept a 4-digit number between at least 1000-2029
    year = r"\b[1-2][0-9]{3}\b"
    # month should accept month names or month numbers
    jan = r"\b[jJ]an(?:uary)?\b"
    feb = r"\b[fF]eb(?:ruary)?\b"
    mar = r"\b[mM]ar(?:ch)?\b"
    apr = r"\b[aA]pr(?:il)?\b"
    may = r"\b[mM]ay\b"
    jun = r"\b[jJ]un(?:e)?\b"
    jul = r"\b[jJ]ul(?:y)?\b"
    aug = r"\b[aA]ug(?:ust)?\b"
    sep = r"\b[sS]ep(?:tember)?\b"
    oct = r"\b[oO]ct(?:ober)?\b"
    nov = r"\b[nN]ov(?:ember)?\b"
    dec = r"\b[dD]ec(?:ember)?\b"
    month = rf"(?:{jan}|{feb}|{mar}|{apr}|{may}|{jun}|{jul}|{aug}|{sep}|{oct}|{nov}|{dec})"
    # day should be a number, which may or may not be zero-padded
    day = r"\b[0-9](?:[0-9])?\b"

    return year, month, day


def convert_month(s: str) -> str:
    """Converts a string month to number (e.g. 'September' -> '09'.

    You don't need to use this function,
    but you may find it useful.

    arguments:
        month_name (str) : month name
    returns:
        month_number (str) : month number as zero-padded string
    """
    # If already digit do nothing
    if s.isdigit():
        return s

    # Convert to number as string
    i = month_names.index(s)+1
    if i < 10:
        return f"0{i}"
    return f"{i}"


def zero_pad(n: str) -> str:
    """zero-pad a number string

    turns '2' into '02'

    arguments:
        n (str): day number
    returns:
        n (str): day number as zero-padded string
    """
    if len(n) == 1:
        return f"0{n}"
    return n


def find_dates(text: str, output: str = None) -> list:
    """Finds all dates in a text using reg ex

    arguments:
        text (string): A string containing html text from a website
    return:
        results (list): A list with all the dates found
    """
    year, month, day = get_date_patterns()

    # Date on format YYYY/MM/DD - ISO
    ISO = rf"{year}-[0-1][0-9]-{day}"

    # Date on format DD/MM/YYYY
    DMY = rf"{day}\s{month}\s{year}"

    # Date on format MM/DD/YYYY
    MDY = rf"{month}\s{day},\s{year}"

    # Date on format YYYY/MM/DD
    YMD = rf"{year}\s{month}\s{day}"

    # list with all supported formats
    formats = rf"(?:{ISO}|{MDY}|{YMD}|{DMY})"
    dates = []

    # find all dates in any format in text
    all_dates = re.findall(formats, text)

    for date in all_dates:
        temp = re.sub(",", "", date)
        arr = re.split(r"(?:\s|-)", temp)
        # If month is first, it is MDY
        if re.search(month, arr[0]):
            dates.append(f"{arr[2]}/{convert_month(arr[0])}/{zero_pad(arr[1])}")
        # If year is first, it is ISO or YMD
        elif re.search(year, arr[0]):
            dates.append(f"{arr[0]}/{convert_month(arr[1])}/{zero_pad(arr[2])}")
        # Else it is DMY
        else:
            dates.append(f"{arr[2]}/{convert_month(arr[1])}/{zero_pad(arr[0])}")

    # Write to file if wanted
    if output:
        with open (output, "w") as f:
            for date in dates:
                f.write(date)

    return dates
