from bottle import get, post, request, run, route, template, response, static_file, redirect, app, error, abort
from beaker.middleware import SessionMiddleware
from collections import OrderedDict
from numpy import inf
import multiprocessing
import bottle
import httplib2
import redis
import operator
import spell
import bjoern

@error(404)
def error404(error):
    return template('error404')

@route('/<filename:re:.*\.jpg>')
def serve_jpg(filename):
        return static_file(filename, root='./', mimetype='image/jpg')
    
@get('/<filename:re:.*\.png>')
def serve_png(filename):
        return static_file(filename, root='./', mimetype='image/png')

@get('/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='./')


@get('/')
def index():
    keywords = request.query.keywords
    
    r_server = redis.Redis(host="localhost", port=6379)
    if keywords:
        url = "?" + request.query_string
        page = request.query.page
        if not page:
            # redirect to page 1
            url += "&page=1"
            redirect(url)

        word_ids = {}
        words = keywords.split()
        corrected_words = []
        doc_ids = {}
        
        # running spellcheck on the query
        for w in words:
            corrected = spell.correction(w)
            if corrected and corrected != w:
                corrected_words.append((corrected, True))
            else:
                corrected_words.append((w, False))
            
        # multiword search, aggregate all the documents and reorder based on number of appearances
        doc_scores = {}
        for w in words:
            w_id = r_server.get("word:%s:word_id" %w)
            doc_ids = r_server.zrevrange("word_id:%s:doc_ids" %w_id, 0, -1)
            for doc in doc_ids:
                score = r_server.get("doc_id:%s:score" %doc)
                #note the number of searched words that appear for that doc
                if doc in doc_scores:
                    doc_scores[doc] = (doc_scores[doc][0], doc_scores[doc][1]+1)
                else:
                    doc_scores[doc] = (score,1)
        
        #sort first by # appearances, then by pagerank score
        sorted_doc_ids = sorted(doc_scores.items(), key=lambda x: (x[1][1], x[1][0]), reverse=True)
            
        # else page number exists
        # strip page number from url
        url = url.split('&')[0]
        # get five results, with start offset by page number
        page = int(page)
        p_start = (page - 1) * 5
        p_end = p_start + 4
        zlen = len(sorted_doc_ids)
        if p_end > zlen:
            p_end = zlen
        doc_ids = sorted_doc_ids[p_start:p_end+1]
        docs = [r_server.get("doc_id:%s:doc" %doc_id[0]) for doc_id in doc_ids]
        titles = [r_server.get("doc_id:%s:title" %doc_id[0]) for doc_id in doc_ids]
        return template('query_results', page = page, url = url, docs = docs, titles=titles, zlen = zlen, query = keywords, corrected = corrected_words)
    else:
        return template('query_page')

session_opts = {
        'session.type': 'cookie',
        'session.cookie_expires': False,
        'session.validate_key': 'validate',
        'session.encrypt_key': 'encrypt',
        'session.auto': True
}
app = SessionMiddleware(app(), session_opts)

def server(port):
	run(server="bjoern", app=app, host='localhost', port=port)

#run(server="bjoern", app=app, host='0.0.0.0', port=80)
jobs = []
for i in range(8):
	p = multiprocessing.Process(target=server, args=(8080+i,))
	p.start()
	jobs.append(p)
for p in jobs:
	p.join()
