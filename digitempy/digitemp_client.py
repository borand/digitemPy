'''
Created on 2012-12-19

@author: borand
'''
import xmlrpclib
import argparse
from common import get_host_ip

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process Input arguments, specify optional server ip and port number')
    parser.add_argument('--ip', default=get_host_ip(), type=str, help='IP of digitemp server')
    parser.add_argument('--port', default=8890, type=int)
    
    args = parser.parse_args()     
    server_address = 'http://%s:%d' % (args.ip, args.port)
    RemoteDigitemp = xmlrpclib.ServerProxy(server_address)
    try:
        print "Sending ping to remote digitemp server at %s" % server_address
        ping_response = RemoteDigitemp.ping()
        
        print "Asking for Data"
        data_set = RemoteDigitemp.GetData()
            
        for data in data_set:
            print "Serial number %s, Temperature %f C" % (data[1], data[2])
    except Exception as inst:
        print type(inst)
        print inst.args
        print inst