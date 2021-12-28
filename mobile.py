###################################################################
# mobile.py
#  
# This python module contains the declarations and defintions of 
# mobile Class and its methods
#
# Author: @Uttej
# Date:   20th Nov 2021
#
# ENTS656 Python project
#
###################################################################

class Mobile:

    def __init__(self, ID, height, HOm, rxThreshold):
        """ Constructor is called when instantiating the object """

        self._ID = ID                  # mobile id
        self._height = height          # height of the mobile 
        self._handOffMargin = HOm      # Handoff margin
        self._rxThreshold = rxThreshold # Rx threshold

        self.position = 0              # position on the road from left to right
        self.direction = 0             # +1 if moving from left to right, else -1
        self.speed = 0                 # in meter per sec
        self.bIsCallActive = False     # boolean variable to indicates the call status 
        self.callDurationLeft = 0      # time left in seconds
        self.connectedBstn = None      # ID of the base station it is connected with


    def reset(self):
        """ This function resets the values to factory defaults """

        self.position = 0
        self.direction = 0
        self.speed = 0
        self.bIsCallActive = False
        self.callDurationLeft = 0
        self.connectedBstn = None
        return
    
    def dump(self):
        print("ID = ", self._ID)
        print("position = ", self.position)
        print("direction = ", self.direction)
        print("speed = ", self.speed)
        print("call active = ", self.bIsCallActive)
        print("call duration left =", self.callDurationLeft)
        print("connected base station = ", self.connectedBstn)

    def getID(self):
        return self._ID

    def getHeight(self):
        return self._height

    def getHandOffMargin(self):
        return self._handOffMargin

    def getRxThreshold(self):
        return self._rxThreshold

    def getPosition(self):
        return self.position

    def setPosition(self, position):
        self.position = position
        return

    def getDirection(self):
        return self.direction

    def setDirection(self, direction):
        self.direction = direction
        return

    def getSpeed(self):
        return self.speed

    def setSpeed(self, speed):
        self.speed = speed
        return

    def isCallActive(self):
        return self.bIsCallActive

    def setCallActive(self, status):
        self.bIsCallActive = status
        return

    def getCallDurationLeft(self):
        return self.callDurationLeft

    def setCallDurationLeft(self, duration):
        self.callDurationLeft = duration
        return

    def getConnectedBstnID(self):
        return self.connectedBstn

    def setConnectedBstnID(self, bstnID):
        self.connectedBstn = bstnID
        return


