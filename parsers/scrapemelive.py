from collectors import basic
import json
import repo

def allow_url_filter(url):
    return '/shop/page/' in url and '#' not in url

def get_html(url):
    return basic.get_html(url)

def extract_content(url,soup):
    return [{
        'id':product.find('a',attrs={'data-product_id':True})['data-product_id'],
        'name':product.find('h2').text,
        'price':product.find(class_='amount').text
    } for product in soup.select('.product')]

def store_content(url,content):
    for item in content:
        if item['id']:
            repo.set_content(item['id'],json.dumps(item))