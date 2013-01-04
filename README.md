DigitemPy
=========

Python modules for interfacing with 1-wire devices via DigiTemp software written by Brian C. Lane
https://github.com/bcl/digitemp.git
   
Introduction 
============

I mainly use this package on my rasberry pi where I run digitemp_server.py.
In most of my measurements I simply need to collect readings from all devices collected to the bus.  

Words of caution  
================

* All code written by beginer with limited experience in python and linux - constructive criticism is appreciated.

* Only tested on lubuntu, ubuntu and rasberry pi (wheezy image)

* The user running the code must be able to run sodo without password (requirement of sh package).  In my case I append lines below
  to the /etc/sudoers file.     

	 includedir /etc/sudoers.d   
	 myusername ALL= NOPASSWD: ALL   

Usage
=====

Install digitemp using apt-get
	
	sudo apt-get install digitemp   

Install virtualenv if it is not already installed

	pip install virtualenv   

Clone the repository  

	git clone https://github.com/borand/digitemPy.git   
	cd digitemPy   
	source venv.sh   

At this point the virtual environment should be activated, install required packages
	
	pip install -r requirements.pip

The code was tested with digitemp DS9490R [Digikey part](http://www.digikey.com/product-search/en/programmers-development-systems/accessories/2621524?k=DS9490R) (usb-1wire bus). Assuming that the device is plugged into the USB port.

	 cd digitemp   
	  python digitemp.py   
	 
	  Checking if digitemp_DS2490 is installed True   
	  Found connected devices:  True   
	  Device is configured:  True   
	  Found config path /home/digitemPy/digitempy/../config/:  False   
	  Found config file digitemp.conf:  False   
	  Saving parsed file to:  /home/digitemPy/digitempy/../config/digitemp.conf   
	  DigiTemp v3.5.0 Copyright 1996-2007 by Brian C. Lane   
	  GNU Public License v2.0 - http://www.digitemp.com   
	  Found DS2490 device #1 at 002/022   
	  Turning off all DS2409 Couplers   
	  ..   
	  Searching the 1-Wire LAN   
	  10F237C0010800D6 : DS1820/DS18S20/DS1920 Temperature Sensor   
	  ROM #0 : 10F237C0010800D6   
	
	  [[0, '10F237C0010800D6', 20.3125]]   
	
Starting the server

	(venv)~/digitemPy/digitempy$ python digitemp_server.py    
	 Checking if digitemp_DS2490 is installed True   
	 Found connected devices:  True   
	 Device is configured:  True   
	 Found config path /home/digitemPy/digitempy/../config/:  True   
	 Found config file digitemp.conf:  True   
	 Starting Digitemp server on ip=192.168.1.106, port=8890   

You can now read the temperature on a remote pc.  The client code uses only standard python modules.

	python digitemp_client.py --ip 192.168.1.106 --port 8890   
	 Sending ping to remote digitemp server at http://192.168.1.106:8890   
	 Asking for Data   
	 Serial number 10F237C0010800D6, Temperature 21.812500 C   

References
==========

https://github.com/bcl/digitemp.git
https://github.com/lekv/digitemp-metricfire.git
