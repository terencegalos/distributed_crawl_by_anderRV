from redis import Redis

connection = Redis(db=1)

to_visit_key = 'crawling:to_visit'
visited_key = 'crawling:visited'
queued_key = 'crawling:queued'
content_key = 'crawling:content'


def count_visited():
    return connection.scard(visited_key)

def count_queued():
    return connection.scard(queued_key)

def pop_to_visit_blocking(timeout=0):
    return connection.blpop(to_visit_key,timeout)

def move_from_queued_to_visited(value):
    return connection.smove(queued_key,visited_key,value)


def add_to_queue(value):
    return connection.sadd(queued_key,value)

def is_queued(value):
    return connection.sismember(queued_key,value)

def is_visited(value):
    return connection.sismember(visited_key,value)

def add_to_visit(value):
    if connection.execute_command('LPOS',to_visit_key,value) is None:
        return connection.rpush(to_visit_key,value)
    
def set_content(key,value):
    connection.hset(content_key,key=key,value=value)