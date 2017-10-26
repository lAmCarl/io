Python script for launching EC2 instance: aws_script.py

Source code of frontend with Google Login API: frontend.py

Public IP Address of live server: 52.70.141.11

Enabled Google API: OAuth2 API

Benchmark Setup:
All benchmarking was performed on a separate AWS t2.micro instance in the same region. This benchmarking instance lives at: 34.231.37.90.

The Apache benchmarking tool, ab, was used. After testing various concurrency levels, 11 was determined to be the highest stable level (ie. did not cause any time-outs during any given run). We did not attempt any improvements on this performance. This was the concurrency used while measuring resource utilization. The command used was:

  $ ab -n 1000 -c 11 http://52.70.141.11/?keywords=helloworld+foo+bar

For resource utilization monitoring, dstat was used, as well as vmstat for more detailed memory usage. The commands were:

  $ dstat -cdn --top-cpu --top-mem --output stats.csv > /dev/null &
  $ vmstat 1 > mem.txt &

The monitoring ran in the background with outputs every second, which were piped to files. After the Apache benchmarking tool was run, the process would be brought to the foreground, then killed using <Ctrl-C>. 

Results can be found in the RESULTS.pdf file.

---------------------------------------------------------------------------------------
For Lab 1:
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

