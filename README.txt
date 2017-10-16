################################
Running the frontend:
  $ python frontend.py

################################
Testing the backend:
Backend can be tested by running

  $ python test_crawler.py

This sets up a local bottle server and runs a crawler on some sites.
urls.txt contains two urls ('/googleca' and '/bing'), one of those urls links to a 3rd ('/google')

googleca contains 3 words: canada search google
google contains 2 words: google search
bing contains 2 words: bing search

The above is the order that urls are crawled and the order of the words in the urls
  Therefore doc_id mapping should be so {1=googleca, 2=google, 3=bing}
  and word_id mapping should be {1=canada, 2=search, 3=google, 4=bing}

The result from the tester should be:
  {1: set([1]), 2: set([1, 2, 3]), 3: set([1, 2]), 4: set([3])}
  {'canada': set(['http://localhost:8080/googleca']), 'search': set(['http://localhost:8080/googleca', 'http://localhost:8080/bing', 'http://localhost:8080/google']), 'google': set(['http://localhost:8080/googleca', 'http://localhost:8080/google']), 'bing': set(['http://localhost:8080/bing'])}
Looking at the results you can see that the above mapping is correct

