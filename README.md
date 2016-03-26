# Beholder
This project is based on the [yowsup-commandserver] (https://github.com/jorgehortelano/yowsup-commandserver) extension for yowsup. The scope is to control a raspberry device that has one or more sensors for motion or sound detection.

This software has been developed using a Raspberry Pi 2 Model B with a LM393 Sound Detection Sensor Module and a Pyroelectric Infrared PIR Motion Sensor Detector Module HC-SR501. The operating system is an Ubuntu Mate.

## Installation

Install [yowsup](https://github.com/tgalal/yowsup/tree/develop) from the develop branch. (This software has been created using version 2.4.48).

After installing yowsup. Install this extension running inside the application folder the next command:
```
python setup.py install
```

## Config
Create a configuration file where the whatsapp credentials are, as in other examples of yowsup. Please follow up [yowsup documentation](https://github.com/tgalal/yowsup/wiki/yowsup-cli-2.0) for registration.
At the end you will have something like:

	cc=39
	phone=39111111111
	password=c5NWTzOrsgCRQr77Yhwafdj+Tgg=

You need to add a set of new parameters:

`allowed_users` parameter define which phone numbers can send commands to the server. 

`alias` parameter is the name of the device that will be shown in the whatsapp messages. 

`pir_pin` parameter is the pin number ([BCM mode](https://pinout.xyz/)) of the raspberry where the signal wire of the Infrared motion sensor is attached.

`sound_pin` parameter is the pin number ([BCM mode](https://pinout.xyz/)) of the raspberry where the signal wire of the sound sensor is attached. 

An example of these parameters:

	allowed_users = ['39111222333@s.whatsapp.net']
	alias = TheEye
	pir_pin = 4
	sound_pin = 17

## Execution

To launch the application execute:

	beholder run -c <file.config>
	
Where the file.config is the previous defined configuration file.

If everything is running, from your whatsapp application, you can use the next messages as commands:

	hello		will show the name (alias) of the device.
	select <alias>	select the device to accept other commands.
	enable		start the sensor detection for the selected device.
	disable		stops sending alerts from sensors.
	help            shows these options.

For using this application at least you need to select the node first, and then start the detection. 
