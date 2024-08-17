from parsers import scrapemelive,defaults
from urllib.parse import urlparse

parsers = {
    'scrapeme.live':scrapemelive,
}

def get_parser(url):
    hostname = urlparse(url).hostname # extract domain from URL

    if hostname in parsers:
        return parsers[hostname]
    
    return defaults