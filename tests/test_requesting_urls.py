# Test with no params
import pytest
from bs4 import BeautifulSoup
from requesting_urls import get_html


@pytest.mark.parametrize(
    "url, expected",
    [
        ("https://en.wikipedia.org/wiki/Studio_Ghibli", "Studio Ghibli"),
        ("https://en.wikipedia.org/wiki/Star_Wars", "Star Wars"),
        ("https://en.wikipedia.org/wiki/Dungeons_%26_Dragons", "Dungeons"),
    ],
)
def test_get_html_no_params(url, expected):
    html = get_html(url)
    assert isinstance(html, str)
    assert "<!DOCTYPE" in html
    assert "<html" in html
    assert expected in html
