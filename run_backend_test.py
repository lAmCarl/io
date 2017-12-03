import multiprocessing
import time
import redis
import pprint
import crawler_threaded
import crawler
from bottle import route, run, template

@route('/A')
def A():
    return '<html><a href="/B">Bat</a><a href="/C">Cat</a><a href="/D">Dat</a></html'

@route('/B')
def B():
    return '<html><a href="/C">Cat</a><a href="/D">Dat</a></html'

@route('/C')
def C():
    return '<html><a href="/D">Dat</a></html'

@route('/D')
def D():
    return '<html><a href="/D">Dat</a></html'

def server():
    run(host='localhost', port=8080)
    return

def tester():
    bot = crawler.crawler(None, "urls.txt")
    #bot = crawler_threaded.crawler(None, "urls.txt")
    bot.crawl(depth=1)
    
    myList = [(bot.get_score(doc_id), doc) for doc_id,doc in bot._doc_cache.items() if doc_id in bot._doc_to_word]
    myList.sort(reverse=True)
    pprint.pprint(myList, width=140)
        
    return

if __name__ == "__main__":
    jobs = []
    p1 = multiprocessing.Process(target=server)
    jobs.append(p1)
    p2 = multiprocessing.Process(target=tester)
    jobs.append(p2)
    p1.start()
    time.sleep(1)
    p2.start()
    p2.join()
    p1.terminate()
    p1.join()
    

