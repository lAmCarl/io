import bottle
from bottle import get, post, request, run, route, template, response, static_file, redirect, app
from oauth2client.client import flow_from_clientsecrets
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from collections import OrderedDict
from beaker.middleware import SessionMiddleware
import httplib2

auth_db = {}
history_db = {}
signedin = False

session_opts = {
        'session.type': 'cookie',
        'session.cookie_expires': False,
        'session.validate_key': 'validate',
        'session.encrypt_key': 'encrypt',
        'session.auto': True
}
app = SessionMiddleware(app(), session_opts)

@route('/<filename:re:.*\.jpg>')
def serve_jpg(filename):
        return static_file(filename, root='./', mimetype='image/jpg')
    
@get('/<filename:re:.*\.png>')
def serve_png(filename):
        return static_file(filename, root='./', mimetype='image/png')

@get('/signin')
def signin():
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
    if token:
        print "session token:"+token
    
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
    elif user and user in auth_db:
        print "server token:" + auth_db[user][0]

    if keywords:
        word_count = OrderedDict()
        words = keywords.split()
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
        return template('parse_query', user=user, query = keywords, word_count = word_count, history=history_db.get(user, None))
    else:
        return template('query_page', user=user, history=history_db.get(user, None))

@route('/redirect')
def redirect_page():
    s = request.environ.get('beaker.session')
    code = request.query.get('code', '')
    
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

run(app=app)
