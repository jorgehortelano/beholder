# Beholder
This project is based on the [yowsup-commandserver] (https://github.com/jorgehortelano/yowsup-commandserver) extension for yowsup. The scope is to control a group of raspberry device each of them has one or more sensors for motion or sound detection.

## Installation

Install [yowsup](https://github.com/tgalal/yowsup/tree/develop) from the develop branch. (This is created for version 2.4.48)

After installing yowsup. Install this extension running:
```
python setup.py install
```

## Config
Create a configuration file where the whatsapp credentials are, as in other examples of yowsup. Something like:

	cc=39
	phone=39111111111
	password=c5NWTzOrsgCRQr77Yhwafdj+Tgg=
	allowed_users = ['39111222333@s.whatsapp.net']
	alias = TheEye

Note: Allowed_users parameters define which phone numbers can send commands to the server. 

## Execution

To launch the application execute:

	beholder run -c <file.config>
	
Where the file.config is the previous defined configuration file.


