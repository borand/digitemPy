'''
Created on 2012-12-19
@author: borand
'''

from SimpleXMLRPCServer import SimpleXMLRPCServer
import digitemp
try:
    import requests
except:
    pass  

D = digitemp.Digitemp()
D.GetData()

def GetData():
    return D.GetData()

def GetSubmitData():
    return D.GetData()

def ping():
    return 'pong'

def main(host='localhost', port=8888):
    server = SimpleXMLRPCServer((host, port))
    server.register_introspection_functions()
    server.register_function(ping)
    server.register_function(GetData)    
    server.register_function(GetSubmitData)
    server.serve_forever()

if __name__ == "__main__":
    main()
