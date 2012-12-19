'''
Created on 2012-12-19
@author: borand
'''

from SimpleXMLRPCServer import SimpleXMLRPCServer
import digitemp 

D = digitemp.Digitemp()
D.GetData()

def GetData():
    
    try:
        data = D.GetData()
        print data
    except:
        print "Error in get data"
        data = []
    
    return data

def ping():
    return 'pong'

server = SimpleXMLRPCServer(('localhost', 8888))
server.register_introspection_functions()
server.register_function(ping)
server.register_function(GetData)

server.serve_forever()