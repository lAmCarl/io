from bottle import get, post, request, run, route, template, response, static_file
from collections import OrderedDict

first = True

@route('/<filename:re:.*\.jpg>')
def serve_picture(filename):
        return static_file(filename, root='./', mimetype='image/jpg')
    
@get('/<filename:re:.*\.png>')
def serve_png(filename):
        return static_file(filename, root='./', mimetype='image/png')

@get('/')
def search():
	keywords = request.query.keywords

	#Clear cookies when server is first launched, otherwise grab from history
	global first
	if first:
		response.set_cookie('history', {}, secret='secret')
		first = False
		history = OrderedDict()
	else:
		history = request.get_cookie('history', secret='secret')

	if keywords:
		word_count = OrderedDict()
		words = keywords.split()
		#increment keywords in current search and search history
		for w in words:
			word_count.setdefault(w.lower(), 0)
			word_count[w.lower()] += 1
			history.setdefault(w.lower(), 0)
			history[w.lower()] += 1
		response.set_cookie('history', history, secret='secret')
		return template('parse_query', query = keywords, word_count = word_count)

	else:	
		return template('query_page', history = history)

run(host='localhost', port=8080, debug=True)
