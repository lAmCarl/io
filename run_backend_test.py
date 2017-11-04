import multiprocessing
import time
import redis
import pprint
from crawler import crawler
from bottle import route, run, template

@route('/googleca')
def googleca():
    return '<html><a href="http://localhost:8080/google">canada search google</a></html'

@route('/google')
def google():
    return '<html><h1>google search</h1></html>'

@route('/bing')
def bing():
    return '<html><h1>bing search</h1></html>'


def server():
    run(host='localhost', port=8080)
    return

def tester():
    bot = crawler(None, "urls.txt")
    bot.crawl(depth=3)
    
    myList = [(doc, bot.get_score(doc_id)) for doc_id,doc in bot._doc_cache.items()]
    myList.sort(reverse=True, key= lambda x: x[1])
    pprint.pprint(myList)
        
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
    time.sleep(1)
    p1.terminate()
    p1.join()
    p2.join()
    

