from bs4 import BeautifulSoup
import repo
from urllib.parse import urljoin

#url,max_items,parser.get_html,parser.extract_content
def crawl(url,max_items,queued_count,get_html,extract_content):
    print(f'Crawling url {url}')
    if not url:
        print(f'URL not provided {url}')
        return
    
    already_seen = _seen(url)
    if already_seen:
        print(f'URL already seen {already_seen}')
        return
    
    total = queued_count + repo.count_visited() + repo.count_queued()

    if total >= max_items:
        print(f'Exiting! queued + visited over maximum: {queued_count,total}')
        return
    
    repo.add_to_queue(url)
    links, content = _crawl(url,get_html,extract_content)
    repo.move_from_queued_to_visited(url)
    return links, content





def add_results_to_queue(urls,allow_url_filter):
    if not urls:
        print(f"Not a url list: {urls}. No url to be added.")
        return
    
    for url in urls:
        print(f'Check url to add -> {url}')
        if allow_url_filter(url) and not _seen(url):
            print(f'Add URL to visit queue {url}')
            repo.add_to_visit(url)


def _seen(url):
    return repo.is_visited(url) or repo.is_queued(url)

def _crawl(url,get_html,extract_content):
    print(f'Crawl -> {url}',)

    html = get_html(url)
    soup = BeautifulSoup(html,'html.parser')
    

    links = _extract_links(url,soup)
    # print(links)
    content = extract_content(url,soup)
    # print(content)

    return links,content

def _extract_links(url,soup):
    return [
        urljoin(url,a.get('href'))
        for a in soup.find_all('a')
        if a.get('href') and not(a.get('rel') and 'nofollow' in a.get('rel'))
    ]