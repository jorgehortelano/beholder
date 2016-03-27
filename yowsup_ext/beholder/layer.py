import os
import string
import subprocess
from yowsup.layers.interface                           import YowInterfaceLayer, ProtocolEntityCallback
import RPi.GPIO as gpio
import time
import sys

class BeholderLayer(YowInterfaceLayer):
    __allowed_users = []
    __alias = ""
    __node_enabled = False
    __node_selected = False
    #Define raspberry gpio input/output
    __pir_pin = 0
    __sound_pin = 0
    __events_initialized = False
    
    def __init__(self, allowed_users, alias, pir_pin, sound_pin):
        super(BeholderLayer, self).__init__()
        self.__allowed_users = allowed_users
        self.__alias = alias
        self.__pir_pin = pir_pin
        self.__sound_pin = sound_pin
        #Define raspberry gpio input/output
        gpio.setmode(gpio.BCM)
        gpio.setup(self.__pir_pin, gpio.IN)
        gpio.setup(self.__sound_pin, gpio.IN)


    #Executes a command if the user is in the allowed_user list. 
    def executeCommand(self, messageProtocolEntity, command):	
        status = subprocess.check_output(command)
        print("Status: "+status)
        messageProtocolEntity.setBody(status)
        self.toLower(messageProtocolEntity.forward(messageProtocolEntity.getFrom()))

    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):
        if messageProtocolEntity.getType() == 'text':
            self.onTextMessage(messageProtocolEntity)
        elif messageProtocolEntity.getType() == 'media':
            self.onMediaMessage(messageProtocolEntity)

        self.toLower(messageProtocolEntity.ack())
        self.toLower(messageProtocolEntity.ack(True))

    def selectNode(self,messageProtocolEntity):
       print("Selecting node: "+ self.__alias)
       self.__node_selected = True
       messageProtocolEntity.setBody("Selecting node '"+ self.__alias+"'")
       self.toLower(messageProtocolEntity.forward(messageProtocolEntity.getFrom()))

       if self.__events_initialized == False :
           try:
               self.__events_initialized = True
               if self.__pir_pin > 0 :
                   gpio.add_event_detect(self.__pir_pin, gpio.RISING, callback=lambda x: self.motion_sensor(self.__pir_pin, messageProtocolEntity), bouncetime=500)
               if self.__sound_pin > 0 :
                   gpio.add_event_detect(self.__sound_pin, gpio.RISING, callback=lambda x: self.sound_sensor(self.__sound_pin, messageProtocolEntity), bouncetime=500)
           except KeyboardInterrupt:
               print("\n"+ self.__alias +" down")
               sys.exit(0)

    def unselectNode(self,messageProtocolEntity):
       print("Unselecting node: "+ self.__alias)
       self.__node_selected = False
       messageProtocolEntity.setBody("Unselecting node '" + self.__alias + "'")
       self.toLower(messageProtocolEntity.forward(messageProtocolEntity.getFrom()))


    def disableNode(self,messageProtocolEntity):
       if self.__node_enabled == True : 
           self.__node_enabled = False
           print("Disabling node: "+ self.__alias)
           messageProtocolEntity.setBody("Disabling node '"+ self.__alias + "'")
           self.toLower(messageProtocolEntity.forward(messageProtocolEntity.getFrom()))

    def sayHello(self,messageProtocolEntity):
        messageProtocolEntity.setBody("Hello from '"+ self.__alias+"'")
        self.toLower(messageProtocolEntity.forward(messageProtocolEntity.getFrom()))

    def enableNode(self,messageProtocolEntity):
       if self.__node_enabled == False :
           self.__node_enabled = True
           print("Enabling node: " + self.__alias)
           messageProtocolEntity.setBody("Enable node '" + self.__alias + "'")
           self.toLower(messageProtocolEntity.forward(messageProtocolEntity.getFrom()))

    def motion_sensor(self, pir_pin, messageProtocolEntity):
        if self.__node_enabled == True :
            messageProtocolEntity.setBody("Motion detected in '" + self.__alias + "'")
            self.toLower(messageProtocolEntity.forward(messageProtocolEntity.getFrom()))

    def sound_sensor(self, sound_pini, messageProtocolEntity):
        if self.__node_enabled == True :
            messageProtocolEntity.setBody("Sound detected in '" + self.__alias + "'")
            self.toLower(messageProtocolEntity.forward(messageProtocolEntity.getFrom()))

    def showHelp(self, messageProtocolEntity):
        messageProtocolEntity.setBody("Available commands:\n\thello\n\tselect <alias>\n\tenable\n\tdisable")
        self.toLower(messageProtocolEntity.forward(messageProtocolEntity.getFrom()))

    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        self.toLower(entity.ack())

    def onTextMessage(self,messageProtocolEntity):
        if messageProtocolEntity.getFrom() in self.__allowed_users:
            if "help" in string.lower(messageProtocolEntity.getBody()):
                self.showHelp(messageProtocolEntity)
            #Node list
            elif "hello" in string.lower(messageProtocolEntity.getBody()): 
                self.sayHello(messageProtocolEntity)
            #Enable/Disable node if needed.
            elif "unselect" in string.lower(messageProtocolEntity.getBody()):
                self.unselectNode(messageProtocolEntity)
            elif "select" in string.lower(messageProtocolEntity.getBody()):
                if string.lower(self.__alias) in string.lower(messageProtocolEntity.getBody()):
                    self.selectNode(messageProtocolEntity)
            elif "disable" in string.lower(messageProtocolEntity.getBody()):
                if self.__node_selected == True:
                    self.disableNode(messageProtocolEntity)
            elif "enable" in string.lower(messageProtocolEntity.getBody()):
                if self.__node_selected == True:
                    if self.__node_enabled == False :
                        self.enableNode(messageProtocolEntity)
            # Execute command if possible.
            elif string.lower(messageProtocolEntity.getBody()) == "reboot":
                if self.__node_selected == True :
                    command = ['sudo', 'reboot']
                    self.executeCommand(messageProtocolEntity, command)
            else:
                # just print info
                if self.__node_selected == True :
                    print("Invalid command '%s' from %s" % (messageProtocolEntity.getBody(), messageProtocolEntity.getFrom(False)))
                    messageProtocolEntity.setBody("Invalid command '%s'." % messageProtocolEntity.getBody() )
                    self.toLower(messageProtocolEntity.forward(messageProtocolEntity.getFrom()))
        else:
            print("Not allowed user '%s'" % messageProtocolEntity.getFrom())
            messageProtocolEntity.setBody("Authorization check failed!")
            self.toLower(messageProtocolEntity.forward(messageProtocolEntity.getFrom()))


    #Media messages cannot send commands. 
    def onMediaMessage(self, messageProtocolEntity):
       # do nothing. 
       return
