'''
Created on Feb 10, 2013

@author: borand
'''
from digitemp import Digitemp
import requests
import datetime
import xmlrpclib
import time

if __name__ == '__main__':
    D = Digitemp()
    D = xmlrpclib.ServerProxy('http://192.168.1.124:8890')
    
    while 1:
        data_set = D.GetData()
        date_stamp = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
        print date_stamp
        for data in data_set:
    #        print "Serial Num: %s Temperature %.2f C" % (D.SerialNumberToDec(data[1]), data[2])
            url = 'http://192.168.1.150/sensordata/api/submit/datavalue/%s/sn/%s/val/%.3f' % (date_stamp, data[1], data[2])
            stat = requests.get(url)
            print stat.content
        time.sleep(60)
    