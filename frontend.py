import bottle
from bottle import get, post, request, run, route, template, response, static_file, redirect, app, error, abort
from collections import OrderedDict
from beaker.middleware import SessionMiddleware
import httplib2
import redis
import operator
from numpy import inf
import spell

auth_db = {}
history_db = {}

session_opts = {
        'session.type': 'cookie',
        'session.cookie_expires': False,
        'session.validate_key': 'validate',
        'session.encrypt_key': 'encrypt',
        'session.auto': True
}
app = SessionMiddleware(app(), session_opts)

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
    s = request.environ.get('beaker.session')
    keywords = request.query.keywords
    user = s.get('user', None)
    token = s.get('token', None)
    
    r_server = redis.Redis(host="localhost", port=6379)
    if keywords:
        url = "?" + request.query_string
        page = request.query.page
        if not page:
            # redirect to page 1
            url += "&page=1"
            redirect(url)

        word_count = OrderedDict()
        word_ids = {}
        words = keywords.split()
        corrected_words = []
        doc_ids = {}
        for w in words:
            corrected = spell.correction(w)
            if corrected and corrected != w:
                corrected_words.append((corrected, True))
            else:
                corrected_words.append((w, False))
            
        doc_scores = {}
        for w in words:
            w_id = r_server.get("word:%s:word_id" %w)
            doc_ids = r_server.zrevrange("word_id:%s:doc_ids" %w_id, 0, -1)
            for doc in doc_ids:
                score = r_server.get("doc_id:%s:score" %doc)
                if doc in doc_scores:
                    doc_scores[doc] *= (float(score) * 100)
                else:
                    doc_scores[doc] = float(score) * 100
        
        sorted_doc_ids = sorted(doc_scores.items(), key=operator.itemgetter(1), reverse=True)
            
        # else page number exists
        # strip page number from url
        url = url.split('&')[0]
        # get id from server matching first word of query
        #word_id = r_server.get("word:%s:word_id" %words[0])
        # get five results from server, with start offset by page number
        page = int(page)
        p_start = (page - 1) * 5
        p_end = p_start + 4
        #zlen = r_server.zcount("word_id:%s:doc_ids" %word_id, -inf, +inf)
        zlen = len(sorted_doc_ids)
        print zlen
        if p_end > zlen:
            p_end = zlen
        #doc_ids = r_server.zrevrange("word_id:%s:doc_ids" %word_id, p_start, p_end)
        doc_ids = sorted_doc_ids[p_start:p_end+1]
        docs = [r_server.get("doc_id:%s:doc" %doc_id[0]) for doc_id in doc_ids]
        titles = [r_server.get("doc_id:%s:title" %doc_id[0]) for doc_id in doc_ids]
        return template('query_results', page = page, url = url, docs = docs, titles=titles, zlen = zlen, query = keywords, corrected = corrected_words, word_count = word_count)
    else:
        return template('query_page')


#run(app=app, host='0.0.0.0', port=80)
run(app=app, host='localhost', port=8080)
