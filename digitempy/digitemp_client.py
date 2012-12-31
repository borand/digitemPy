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
import digitemp

from common import get_host_ip

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
    submit = 0
    remote = 1
    
    server_ip = get_host_ip()
    digitemp_server_ip = '192.168.1.124'
    server_ip = '192.168.1.150'
    if remote:
        RemoteDigitemp = xmlrpclib.ServerProxy('http://%s:8890' % digitemp_server_ip)
        print RemoteDigitemp.ping()
        data_set = RemoteDigitemp.GetData()
    else:
        LocalDigitemp = digitemp.Digitemp()
        data_set      = LocalDigitemp.GetData()
#        for ix in range(len(data)):
#            c.submit_data(serial_number=data[ix][1], value=data[ix][2],ip='192.168.1.150')
        
    for data in data_set:
        if submit:        
            res = submit_data(serial_number=data[1], value=data[2], ip=server_ip, port=80)
        else:
            print data[1], data[2]
            
