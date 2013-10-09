import digitemp as dt

from logbook import Logger

##########################################################################################
class DigitempCli(object):
    last_cmd = ''
    """docstring for DigitempCli"""
    def __init__(self):
        self.Log = Logger('DigitempCli')
        self.idn = 'DigitempCli %d' % id(self)
        self.digitemp = dt.Digitemp()

    def __unicode__(self):
        return str(self)

    def send(self, cmd, **kwargs):
        self.Log.debug('send(cmd=%s, kwargs=%s)' %(cmd, str(kwargs)))
        self.last_cmd = cmd

        dt_method = getattr(self.digitemp, cmd)
        dt_method()

        return True

    def read(self, **kwargs):
        self.Log.debug('read(kwargs=%s)' %str (kwargs))
        return (0,'DigitempCli resposne to %s' % self.last_cmd)

    def query(self, cmd, **kwargs):
    	try:
        	dt_method = getattr(self.digitemp, cmd)
        	result = [0, dt_method()]
        except Exception as e:
        	result = [1, e.message]

        return result