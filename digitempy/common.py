'''
Created on 2012-12-21

@author: borand
'''
import sh
import re

def get_host_ip():
    ip_exp = re.compile('(?:inet addr:192.168.)(\d+\.\d+)')
    ip_out = ip_exp.findall(sh.ifconfig().stdout)
    if len(ip_out) == 1:
        return '192.168.' + ip_out[0]
    else:
        return '127.0.0.1'