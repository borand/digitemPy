'''
Created on 2012-12-19
@author: borand
'''


import digitemp
import argparse

from SimpleXMLRPCServer import SimpleXMLRPCServer
from common import get_host_ip

D = digitemp.Digitemp()

def GetData():
    return D.GetData()

def GetSubmitData():
    return D.GetData()

def ping():
    return 'pong'

def main(host=get_host_ip(), port=8890):
    server = SimpleXMLRPCServer((host, port))
    server.register_introspection_functions()
    server.register_function(ping)
    server.register_function(GetData)    
    server.register_function(GetSubmitData)
    server.serve_forever()

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Process Input arguments, specify optional host ip and port number')
    parser.add_argument('--ip', default=get_host_ip(), type=str, help='IP of the server to which digitemp is connected')
    parser.add_argument('--port', default=8890, type=int)
    
    args = parser.parse_args()
    
    print "Starting Digitemp server on ip=%s, port=%d" % (args.ip, args.port)
    main(host=args.ip, port=args.port)
