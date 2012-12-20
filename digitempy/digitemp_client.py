'''
Created on 2012-12-19

@author: borand
'''
import xmlrpclib

RemoteDigitemp = xmlrpclib.ServerProxy('http://localhost:8888')

print RemoteDigitemp.ping()
print RemoteDigitemp.GetData()