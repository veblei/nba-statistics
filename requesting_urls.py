from typing import Dict, Optional

import requests


def get_html(url: str):
    """Get an HTML page and return its contents.

    Args:
        url (str):
            The URL to retrieve.
    Returns:
        html (str):
            The HTML of the page, as text.
    """
    headers = {"User-Agent": "NBA-Statistics-Crawler/1.0"}
    # passing the optional parameters argument to the get function
    response = None
    if (headers):
        response = requests.get(url, headers=headers)
    else:
        response = requests.get(url)

    html_str = response.text

    return html_str