from celery import Celery
from crawler import crawl, add_results_to_queue
from parserlist import get_parser

queue_name = 'celery'
app = Celery('tasks',broker_url='redis://127.0.0.1:6379/1')

app_client = app.connection().channel().client

@app.task
def queue_url(url,max_items):
    queued_count = app_client.llen(queue_name)

    parser = get_parser(url)

    result = crawl(url,max_items,queued_count,parser.get_html,parser.extract_content)
    
    if result is None:
        print(f'Exiting task! No result from this crawl')
        return False
    
    links, content = result

    parser.store_content(url,content)
    add_results_to_queue(links,parser.allow_url_filter)