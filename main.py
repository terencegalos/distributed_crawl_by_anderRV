from tasks import queue_url
import repo

starting_url = 'https://scrapeme.live/shop/page/1/'

repo.add_to_visit(starting_url)

maximum_items = 10

while True:

    total = repo.count_visited() + repo.count_queued()
    if total > maximum_items:
        print('Exiting! Over maximum:',total)
        break

    item = repo.pop_to_visit_blocking(60)

    if item is None:
        print('Timeout! No more items to process')
        break

    url = item[1].decode('utf-8') # decode url from redis
    print('Pop URL ',url)

    queue_url.delay(url,maximum_items)
