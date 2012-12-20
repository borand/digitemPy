'''
Created on 2012-12-19

@author: borand
'''
import xmlrpclib
import datetime
import logging
import requests
import sh
import re

RemoteDigitemp = xmlrpclib.ServerProxy('http://localhost:8888')

def get_host_ip():
    ip_exp = re.compile('(?:inet addr:192.168.)(\d+\.\d+)')
    ip_out = ip_exp.findall(sh.ifconfig().stdout)
    if len(ip_out) == 1:
        return '192.168.' + ip_out[0]
    else:
        return '127.0.0.1'

def submit_data(timestamp=None, serial_number='test-device-instance-001', value=0, ip='192.168.1.150', port=80):
    if timestamp is None:
        timestamp=datetime.datetime.now()
    Request = None    
    
    timestamp = str(timestamp).split('.')[0]
    para = {'datetime':timestamp, 'serial_number':serial_number,'data_value':value}
    logging.info("submit_data: timestamp=%s, submit_data(serial_number=%s, value=%f)" % (timestamp, serial_number, value))
    try:  
        Request = requests.get('http://%s:%d/input' % (ip, port), params=para, timeout=3)
        if Request.ok:
            logging.info("Data submitted, response=" + Request.content)            
        else:
            logging.info("Problems with data submission")
    except Exception, E: 
        #ConnectionError        
        logging.info("Errors during submission process: " + str(E))
    
    return Request.status_code

if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)10s: %(message)10s', level=logging.INFO)   
    print RemoteDigitemp.ping()
    data_set = RemoteDigitemp.GetData()
    for data in data_set:
        print "Sending", data
        res = submit_data(serial_number=data[1], value=data[2], ip=get_host_ip(), port=80)
        print res