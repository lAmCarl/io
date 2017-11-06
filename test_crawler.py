import multiprocessing
import time
import redis
from crawler_threaded import crawler
import crawler as other_crawler
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
    bot.crawl(depth=1)
    r_server = redis.Redis(host="localhost", port=6379)
    #inverted_index = bot.get_inverted_index()
    #resolved_inverted_index = bot.get_resolved_inverted_index()
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
    
