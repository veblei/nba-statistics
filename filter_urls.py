import re
from urllib.parse import urljoin


def find_urls(
    html: str,
    base_url: str = "https://en.wikipedia.org",
    output: str = None,
) -> set:
    """Find all the url links in a html text using regex
    Arguments:
        html (str): html string to parse
    Returns:
        urls (set) : set with all the urls found in html text
    """
    # create and compile regular expression(s)
    a_pat = re.compile(r"<a.*>", flags=re.IGNORECASE)
    href_pat = re.compile(r'href="([^"]+)"', flags=re.IGNORECASE)
    urls = set()

    # 1. find all the anchor tags, then
    # 2. find the urls href attributes
    for a_tag in a_pat.findall(html):
        match = href_pat.search(a_tag)
        if match:
            # Splits the href to remove any fragments from it.
            path = re.split("#", match.group(1))
            # Appends the href to urls if it is already a full url.
            if (re.search("^https", path[0])):
                urls.add(path[0])
            # Adds 'https:' and appends the href if it starts with '//'.
            elif (re.search("^//", path[0])):
                urls.add(f"https:{path[0]}")
            # Adds the base_url and appends the href if it starts with '/'.
            elif (re.search("^/", path[0])):
                urls.add(base_url+path[0])

    # Write to file if requested
    if output:
        print(f"Writing to: {output}")
        with open (output, "w") as f:
            for url in urls:
                f.write(url)

    return urls


def find_articles(html: str, output=None) -> set:
    """Finds all the wiki articles inside a html text. Make call to find urls, and filter
    arguments:
        - text (str) : the html text to parse
    returns:
        - (set) : a set with urls to all the articles found
    """
    urls = find_urls(html)

    for url in urls.copy():
        if (len(re.split(":", url)) > 2):
            urls.remove(url)
        elif not (url.startswith("https://en.wikipedia.org/wiki/")):
            urls.remove(url)

    # Write to file if wanted
    if output:
        with open (output, "w") as f:
            for url in urls:
                f.write(url)
    
    return urls


## Regex example
def find_img_src(html: str):
    """Find all src attributes of img tags in an HTML string

    Args:
        html (str): A string containing some HTML.

    Returns:
        src_set (set): A set of strings containing image URLs

    The set contains every found src attibute of an img tag in the given HTML.
    """
    # img_pat finds all the <img alt="..." src="..."> snippets
    # this finds <img and collects everything up to the closing '>'
    img_pat = re.compile(r"<img[^>]+>", flags=re.IGNORECASE)
    # src finds the text between quotes of the `src` attribute
    src_pat = re.compile(r'src="([^"]+)"', flags=re.IGNORECASE)
    src_set = set()
    # first, find all the img tags
    for img_tag in img_pat.findall(html):
        # then, find the src attribute of the img, if any
        match = src_pat.search(img_tag)
        if match:
            src_set.add(match.group(1))
    return src_set
