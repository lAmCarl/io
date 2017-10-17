from bottle import get, post, request, run, route, template, response, static_file
from oauth2client.client import flow_from_clientsecrets
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build

@route('/', 'GET')
def home():
    flow = flow_from_clientsecrets("client_secret_821968399713-054upuhr0jes67did9u5jhmuadpe7g6v.apps.googleusercontent.com.json",
                                    scope='https://www.googleapis.com/auth/plus.me https://www.googleapis.com/auth/userinfo.email',
                                    redirect_uri="http://localhost:8080/redirect")
    uri = flow.step1_get_authorize_url()
    bottle.redirect(str(uri))
    
@route('/redirect')
def redirect_page():
    code = request.query.get('code', '')
    
    flow = OAuth2WebServerFlow( client_id=CLIENT_ID,
                                client_secret=CLIENT_SECRET,
                                scope=SCOPE,
                                redirect_uri=REDIRECT_URI)
    
    credentials = flow.step2_exchange(code)
    token = credentials.id_token('su')
    
    http = httplib2.Http()
    http = credentials.authorize(http)
    
    # Get user email
    users_service = build('oauth2', 'v2', http=http)
    user_document = users_service.userinfo().get().execute()
    user_email = user_document['email']
    
    return "<html><body>hello "+user_email+"</body></html>"



run(host='localhost', port=8080, debug=True)
