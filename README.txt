DEPLOYING ON AWS
To deploy the web server on an aws instance:
  - Edit config.py with appropriate information
  - Run $ python deployment.py

After running, it will return 3 things:
  - IP to ssh into instance
  - DNS to access website
  - Instance ID to terminate instance

To terminate the instance, run:
  $ python terminate.py <Instance ID>

###########################################################################################
DEPLOYING LOCALLY WITH SCRIPT
If you are running on an Ubuntu machine, you can deploy using the install_pkgs.sh script:
  $ sh install_pkgs.sh

###########################################################################################
MANUAL INSTALLATION AND DEPLOYMENT
Setup and Installation:
  Programs that need to be installed beforehand:
    - pound:
      $ sudo apt-get install pound
      $ sudo cp -rf pound.cfg /etc/pound/pound.cfg
      $ sudo cp -rf pound /etc/default/pound
    - redis:
      $ sudo apt-get install redis-server
      
  Python libraries:
    $ pip install -r requirements.txt

Prepopulating the database:
  If you already have a dump.rdb file, to get redis to pre-populate the database
  next time redis starts, just restart redis service:
  $ sudo service redis-server stop
  $ sudo service redis-server start

Running Pound:
  Pound is used as a proxy and does load balancing across our multiple Bottle server
  To start pound, call:
  sudo /etc/init.d/pound start

Running Redis:
  Before running the backend or frontend, we need to start up the redis server
  $ sudo redis-server

Running the backend:
  To populate the database with new data you need to run the backend.
  First, update urls.txt with the links you want to crawl.
  Update run_backend_test.py to crawl to your desired depth
  Then with the redis server running, call:
    $ python run_backend_test.py
    
Running the frontend:
  Once Pound and the Redis server have been started, frontend can be run by calling:
  $ sudo python frontend.py
