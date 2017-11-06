import bottle
from bottle import get, post, request, run, route, template, response, static_file, redirect, app, error, abort
from oauth2client.client import flow_from_clientsecrets
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
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

@get('/signin')
def signin():
#    flow = flow_from_clientsecrets("client_secret_821968399713-054upuhr0jes67did9u5jhmuadpe7g6v.apps.googleusercontent.com.json", scope='https://www.googleapis.com/auth/plus.me https://www.googleapis.com/auth/userinfo.email', redirect_uri="http://52.70.141.11.xip.io/redirect")
    flow = flow_from_clientsecrets("client_secret_821968399713-054upuhr0jes67did9u5jhmuadpe7g6v.apps.googleusercontent.com.json", scope='https://www.googleapis.com/auth/plus.me https://www.googleapis.com/auth/userinfo.email', redirect_uri="http://localhost:8080/redirect")
    uri = flow.step1_get_authorize_url()
    redirect(str(uri))
    
@get('/signout')
def signout():
    s = request.environ.get('beaker.session')
    s.pop('user', None)
    s.pop('token', None)
    s.save()
    redirect('/')

@get('/')
def index():
    s = request.environ.get('beaker.session')
    keywords = request.query.keywords
    user = s.get('user', None)
    token = s.get('token', None)
    
    if user and user in auth_db and auth_db[user][0] == token:
        credentials = auth_db[user][1]
        if credentials.access_token_expired:
            token = credentials.get_access_token()[0]
            s['token'] = token
            auth_db[user] = (token, credentials)
            s.save()
        http = httplib2.Http()
        http = credentials.authorize(http)
        users_service = build('oauth2', 'v2', http=http)
        user_document = users_service.userinfo().get().execute()
        user_name = user_document['name']

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
                if user:
                    history_db[user]['count'].setdefault(w.lower(), 0)
                    history_db[user]['count'][w.lower()] += 1
                    recents = history_db[user]['recent']
                    if w in recents:
                        recents.remove(w)
                    if len(recents) == 10:
                        recents.pop()
                    recents.insert(0, w)
                    history_db[user]['recent'] = recents
            redirect(url)
        # else page number exists
        # strip page number from url
        url = url.split('&')[0]
        # get id from server matching first word of query
        word_id = r_server.get("word:%s:word_id" %words[0])
        # get five results from server, with start offset by page number
        page = int(page)
        p_start = (page - 1) * 5
        p_end = p_start + 5
        zlen = r_server.zcount("word_id:%s:doc_ids" %word_id, -inf, +inf)
        print zlen
        if p_end > zlen:
            p_end = zlen
        doc_ids = r_server.zrevrange("word_id:%s:doc_ids" %word_id, p_start, p_end)
        docs = [r_server.get("doc_id:%s:doc" %doc_id) for doc_id in doc_ids]
        return template('query_results', page = page, url = url, docs = docs, zlen = zlen, user = user, query = keywords, word_count = word_count, history = history_db.get(user, None))
    else:
        return template('query_page', user = user, history = history_db.get(user, None))

@route('/redirect')
def redirect_page():
    s = request.environ.get('beaker.session')
    code = request.query.get('code', '')
    
#    flow = flow_from_clientsecrets("client_secret_821968399713-054upuhr0jes67did9u5jhmuadpe7g6v.apps.googleusercontent.com.json",
#                                   scope='https://www.googleapis.com/auth/plus.me https://www.googleapis.com/auth/userinfo.email',
#                                    redirect_uri="http://52.70.141.11.xip.io/redirect")
    flow = flow_from_clientsecrets("client_secret_821968399713-054upuhr0jes67did9u5jhmuadpe7g6v.apps.googleusercontent.com.json",
                                    scope='https://www.googleapis.com/auth/plus.me https://www.googleapis.com/auth/userinfo.email',
                                    redirect_uri="http://localhost:8080/redirect")
    credentials = flow.step2_exchange(code)
    token = credentials.id_token['sub']
    
    http = httplib2.Http()
    http = credentials.authorize(http)
    
    # Get user email
    users_service = build('oauth2', 'v2', http=http)
    user_document = users_service.userinfo().get().execute()
    user_email = user_document['email']
    
    s['user'] = user_email
    s['token'] = token
    print token
    auth_db[user_email] = (token, credentials)
    history_db.setdefault(user_email, {'count':{}, 'recent':[]})
    s.save()
    redirect('/')

#run(app=app, host='0.0.0.0', port=80)
run(app=app, host='localhost', port=8080)
