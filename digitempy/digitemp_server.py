'''
Created on 2012-12-19
@author: borand
'''

from SimpleXMLRPCServer import SimpleXMLRPCServer
import digitemp
from common import get_host_ip

try:
    import requests
except:
    pass  

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
    main()
