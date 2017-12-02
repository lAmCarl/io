import bottle
from bottle import get, post, request, run, route, template, response, static_file, redirect, app, error, abort
from collections import OrderedDict
from beaker.middleware import SessionMiddleware
import httplib2
import redis
from numpy import inf

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
        word_count = OrderedDict()
        words = keywords.split()
        if not page:
            # redirect to page 1
            url += "&page=1"
            #increment keywords in current search and search history
            for w in words:
                word_count.setdefault(w.lower(), 0)
                word_count[w.lower()] += 1
            redirect(url)
        # else page number exists
        # strip page number from url
        url = url.split('&')[0]
        # get id from server matching first word of query
        word_id = r_server.get("word:%s:word_id" %words[0])
        # get five results from server, with start offset by page number
        page = int(page)
        p_start = (page - 1) * 5
        p_end = p_start + 4
        zlen = r_server.zcount("word_id:%s:doc_ids" %word_id, -inf, +inf)
        print zlen
        if p_end > zlen:
            p_end = zlen
        doc_ids = r_server.zrevrange("word_id:%s:doc_ids" %word_id, p_start, p_end)
        docs = [r_server.get("doc_id:%s:doc" %doc_id) for doc_id in doc_ids]
        return template('query_results', page = page, url = url, docs = docs, zlen = zlen, query = keywords, word_count = word_count)
    else:
        return template('query_page')


run(app=app, host='0.0.0.0', port=80)
#run(app=app, host='localhost', port=8080)
