import logging
import re
import os
import sh
import simplejson

class Digitemp():
    
    def __init__(self):
        self.is_installed       = 0
        self.username           = sh.whoami().stdout[:-1]
        self.config_file_path   = '/home/%s/digitemp/' % self.username
        self.config_filename    = 'digitemp.conf'
        self.digitemp_cmd_str   = 'digitemp_DS2490'
        self.digitemp           = sh.Command(self.digitemp_cmd_str)        
        self.usb_dev_num        = 0
        self.usb_bus_num        = 0
        self.num_of_sensors     = []
        self.serial_number_list = []       
        self.installed          = self.IsInstalled()
        self.IsConnected()
    
    
    def _DigitempErrorCallback(self,lines):
        return lines
    
    def IsInstalled(self):
        logging.debug("def IsInstalled(self):")
        out = sh.which(self.digitemp_cmd_str)
        if out is None:
            logging.error('digitemp_DS2490 not found on the system, use sudo apt-get install digitemp')
            return False
        else:
            logging.info("Found digitemp_DS2490 in : %s" % out)
            return True
    
    def IsConnected(self):
        logging.debug("def IsConnected(self):")
        ret = sh.lsusb()
        logging.debug(ret.stdout)
        expr = r'Bus (\d+) Device (\d+)\: ID (\w{4}.\w{4}) Dallas Semiconductor (DS\w+) .* 1-Wire adapter'
        device_data = re.findall(expr,ret.stdout)
        if len(device_data) > 0:
            logging.info("Found 1 wire adapter bus: %s, device: %s" % (device_data[0][0],device_data[0][1]) )
            self.usb_bus_num = device_data[0][0]
            self.usb_dev_num = device_data[0][1]
            return True         
        else:
            logging.error('Did not find any devices matching: "%s"' % expr)
            return False
    
    def IsConfigured(self):
        if self.IsConnected() and self.IsInstalled():
            dev_path = '/dev/bus/usb/%s/%s' % (self.usb_bus_num, self.usb_dev_num)
            ret = sh.ls(dev_path,'-l')
            with sh.sudo:
                ret = sh.chmod('777',dev_path)
                ret = sh.modprobe('-r', 'ds2490')            
            print ret
            
        else:
            pass
    
    def GenerateConfigFile(self):
        if os.path.exists(self.config_file_path):
            logging.debug('Config file path found')
        else:
            logging.debug('Config file path not found, attempting to mkdir %s' % self.config_file_path)
            ret = sh.mkdir(self.config_file_path)
            if ret.exit_code == 0:
                logging.debug('Config file created')
            else:
                logging.error("Problems creating config file direcotyr")
            
        ret = self.digitemp('-q','-i','-c %s/digitemp.conf' % self.config_file_path)
        print ret
    
    def ParseConfigFile(self):
        """ Function loads the contents of the digitemp.conf file and parses the contents.
        
        TTY USB
        READ_TIME 1000
        LOG_TYPE 1
        LOG_FORMAT "%b %d %H:%M:%S Sensor %s C: %.2C F: %.2F"
        CNT_FORMAT "%b %d %H:%M:%S Sensor %s #%n %C"
        HUM_FORMAT "%b %d %H:%M:%S Sensor %s C: %.2C F: %.2F H: %h%%"
        SENSORS 9
        ROM 0 0x10 0x30 0xB8 0xD2 0x01 0x08 0x00 0xBC 
        ROM 1 0x10 0x48 0xB7 0xD2 0x01 0x08 0x00 0xEA
         
        """
        
        full_file_name=self.config_file_path + self.config_filename
        if self.ConfigFileExists():
           
            file_content = self.LoadConfigFile()
            
            # Parse the number of sensors in the config file
            sensors_str = re.compile('(?:SENSORS\s+)(\d+)(?:\n)')
            num_of_sensors = int(sensors_str.findall(file_content)[0])
            
            rom_expr = re.compile('(?:ROM\s\d+)(?:\s0x)(\w{2})(?:\s0x)(\w{2})(?:\s0x)(\w{2})(?:\s0x)(\w{2})(?:\s0x)(\w{2})(?:\s0x)(\w{2})(?:\s0x)(\w{2})(?:\s0x)(\w{2})')
            rom_content_hex = rom_expr.findall(file_content)
            serial_number_list = []
            for device in rom_content_hex:
                serial_number_list.append("".join(device))
            
            self.num_of_sensors     = num_of_sensors
            self.serial_number_list = serial_number_list
            config_file_dict = {'full_file_name' : full_file_name,
                            'num_of_sensors' : self.num_of_sensors,
                            'serial_number_list' : self.serial_number_list}
            return config_file_dict
        else:
            logging.error("ReadConfigFile(): '%s' not found on the system" % full_file_name)
            return None
    
    def GetData(self):
        ret = self.digitemp('-a', '-q',  '-c%s' % self.config_file_path + self.config_filename, '-o<data>[%s, "%R", %C]</data>')
        
        data_expr = re.compile('(?:<data>)(\[.*\])(?:</data>)')
        data_vector_str = data_expr.findall(ret.stdout)
        
        number_of_readings = len(data_vector_str)
        num_of_sensors = self.ParseConfigFile().get('num_of_sensors')
        if not number_of_readings == num_of_sensors:
            logging.warning('Number of temperature readings %d is less then number of sensors in the config file %d'
                         %(number_of_readings,num_of_sensors))
        
        data = []
        for reading in data_vector_str:
            data.append(simplejson.loads(reading))
        return data

    def SerialNumberToDec(self, hex_str):
        dec_vector = []
        for i in range(0,len(hex_str),2):
            dec_vector.append(int(float.fromhex(hex_str[i:i+2])))
        return dec_vector    
        
    def GetStatus(self):
        print "Digitemp installed : ", self.IsInstalled()
        print "Device connected   : ", self.IsConnected()
        print "Device configured  : ", self.IsConfigured() 
    
    def ConfigFileExists(self):
        full_file_name=self.config_file_path + self.config_filename
        return os.path.exists(full_file_name)

    def LoadConfigFile(self):
        full_file_name=self.config_file_path + self.config_filename
        if self.ConfigFileExists():
            fid = open(full_file_name, 'r')
            file_content = fid.read()
            fid.close();
        else:
            file_content = ''        
        
        return file_content

            
if __name__ == "__main__":
    #logging.basicConfig(format='%(levelname)10s: %(message)10s', level=logging.INFO)    
    D = Digitemp()
    print D.ParseConfigFile()
    print D.GetData()
    #D.GetStatus()
    #temp = D.GetData()
#    for i in temp:
#        print "Serial Num: %s Temperature %.2f C" % (D.SerialNumberToDec(i[1]), i[2]) 