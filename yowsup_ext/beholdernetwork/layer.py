import os
import string
import subprocess
from yowsup.layers.interface                           import YowInterfaceLayer, ProtocolEntityCallback

class BeholderLayer(YowInterfaceLayer):
    __allowed_users = []
    __alias = ""
    __node_enabled = False
    
    def __init__(self, allowed_users, alias):
        super(BeholderLayer, self).__init__()
        self.__allowed_users = allowed_users
        self.__alias = alias

    #Executes a command if the user is in the allowed_user list. 
    def executeCommand(self, messageProtocolEntity, command):	
        if messageProtocolEntity.getFrom() in self.__allowed_users:	    
            status = subprocess.check_output(command)
            print("Status: "+status)
            messageProtocolEntity.setBody(status)
        else:
            print("Not allowed user '%s'" % messageProtocolEntity.getFrom())
            messageProtocolEntity.setBody("Authorization check failed!")
        self.toLower(messageProtocolEntity.forward(messageProtocolEntity.getFrom()))

    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):

        if messageProtocolEntity.getType() == 'text':
            self.onTextMessage(messageProtocolEntity)
        elif messageProtocolEntity.getType() == 'media':
            self.onMediaMessage(messageProtocolEntity)

        self.toLower(messageProtocolEntity.ack())
        self.toLower(messageProtocolEntity.ack(True))

    def enableNode(self,messageProtocolEntity):
       if self.__node_enabled == False :
           self.__node_enabled = True
           print("Enabling node: "+ self.__alias)
           messageProtocolEntity.setBody("Enabling node: "+ self.__alias)
           self.toLower(messageProtocolEntity.forward(messageProtocolEntity.getFrom()))

    def disableNode(self,messageProtocolEntity):
       if self.__node_enabled == True : 
           self.__node_enabled = False
           print("Disabling node: "+ self.__alias)
           messageProtocolEntity.setBody("Disabling node: "+ self.__alias)
           self.toLower(messageProtocolEntity.forward(messageProtocolEntity.getFrom()))

    def sayHello(self,messageProtocolEntity):
        messageProtocolEntity.setBody("Hello from: "+ self.__alias)
        self.toLower(messageProtocolEntity.forward(messageProtocolEntity.getFrom()))

    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        self.toLower(entity.ack())

    def onTextMessage(self,messageProtocolEntity):
        #Node list
        if "hello" in string.lower(messageProtocolEntity.getBody()): 
            self.sayHello(messageProtocolEntity)
        #Enable/Disable node if needed.
        if "enable" in string.lower(messageProtocolEntity.getBody()):
            if string.lower(self.__alias) in string.lower(messageProtocolEntity.getBody()):
                self.enableNode(messageProtocolEntity)
            else:
                self.disableNode(messageProtocolEntity)
        elif "disable" in string.lower(messageProtocolEntity.getBody()):
            if string.lower(self.__alias) in string.lower(messageProtocolEntity.getBody()):
                self.disableNode(messageProtocolEntity)
        # Execute command if possible.
        elif string.lower(messageProtocolEntity.getBody())=="ls":
            if self.__node_enabled == True :
                command = ['ls', '-l']
                self.executeCommand(messageProtocolEntity, command)
        elif string.lower(messageProtocolEntity.getBody())=="reboot":
            if self.__node_enabled == True :
                command = ['sudo', 'reboot']
                self.executeCommand(messageProtocolEntity, command)
        else:
            # just print info
            if self.__node_enabled == True :
                print("Invalid command '%s' from %s" % (messageProtocolEntity.getBody(), messageProtocolEntity.getFrom(False)))
                messageProtocolEntity.setBody("Invalid command '%s'." % messageProtocolEntity.getBody() )
                self.toLower(messageProtocolEntity.forward(messageProtocolEntity.getFrom()))

    #Media messages cannot send commands. 
    def onMediaMessage(self, messageProtocolEntity):
       # do nothing. 
       return
