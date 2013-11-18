"""digitemp_daq.py - 

Usage:
  digitemp_daq.py localhost [--server=SERVER | --test]
  digitemp_daq.py [--host=IP_ADDRESS | --port=REMOTE_PORT | --server=SERVER | --test] 
  digitemp_daq.py [--host=IP_ADDRESS | --port=REMOTE_PORT]
  digitemp_daq.py (-h | --help)

Options:
  -h, --help
  --server=SERVER     [default: sensoredweb.heroku.com]
  --host=IP_ADDRESS   [default: 192.168.1.11]
  --port=REMOTE_PORT  [default: 8890]
  --test

"""

from digitemp import Digitemp
import requests
import datetime
import xmlrpclib
import time
import logging
from docopt import docopt


if __name__ == '__main__':
    arguments = docopt(__doc__)    
    
    print(arguments)
    if arguments['--test']:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(filename='digitemp_daq.log',level=logging.INFO)
    
    logging.info("Starting")
    if arguments['localhost']:
        logging.info("Using locally attached DS2490")
        D = Digitemp()
    else:
        remote_digitemp = 'http://%s:%s' %(arguments['--host'], arguments['--port'])
        logging.info("Connecting to: " + remote_digitemp)        
        D = xmlrpclib.ServerProxy(remote_digitemp)
    
    done = False
    while not done:
        try:
            data_set = D.GetData()
            date_stamp = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
            logging.info("Submitting on %s" % date_stamp)
            for data in data_set:
        #        print "Serial Num: %s Temperature %.2f C" % (D.SerialNumberToDec(data[1]), data[2])
                url = 'http://%s/sensordata/api/submit/datavalue/%s/sn/%s/val/%.3f' % (arguments['--server'], date_stamp, data[1], data[2])
                logging.debug("Submitting to %s" % url)
                stat = requests.get(url)
                print stat.content
        except:
            logging.error("Will add more details soon")
        
        if arguments['--test']:
            done = True
        time.sleep(60)
    