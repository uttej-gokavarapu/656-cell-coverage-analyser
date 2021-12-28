###################################################################
# basestation.py
#  
# This python module contains the declarations and defintions of 
# baseStation Class and its methods
#
# Author: @Uttej
# Date:   20th Nov 2021
#
# ENTS656 Python project
#
###################################################################

import statRecord as stat

class BaseStation:
    
    def __init__(self, ID, height, location, txPower, lineLoss, \
                 antennaGain, channels, opFreq, tilt, vertDiscrmnData, shadow):
        
        self._ID = ID                              #ID of bstn
        self._height = height                      #height of bstn
        self._location = location                  #location of bstn orthogonal to road
        self._txPower = txPower                    #transmitter power
        self._lineLoss = lineLoss                  #connector line losses
        self._antennaGain = antennaGain            #antenna gain
        self._channels = channels                  #number of channels per sector
        self._opFreq = opFreq                      #operating frequency
        self._tilt = tilt                          #tilt angle of antenna
        self._vertDiscrmnData = vertDiscrmnData[:] #Copying list
        self._shadowValues = shadow.copy()         #Copying Array

        #More initializations
        self._boreEIRP = self._txPower - self._lineLoss + self._antennaGain 
        
        self.freeChannels = self._channels         #Number of free channels
        self.stats = stat.Statistics()             #Statistics object
        
    def getID(self):
        return self._ID

    def getHeight(self):
        return self._height

    def getLocation(self):
        return self._location

    def getOperationalFreq(self):
        return self._opFreq

    def getTilt(self):
        return self._tilt

    def getVertDiscrmnData(self):
        return self._vertDiscrmnData

    def getBoreSightEIRP(self):
        return self._boreEIRP

    def getFreeChanCount(self):
        return self.freeChannels

    def isFreeChanAvailable(self):
        if self.freeChannels > 0:
            return True
        else:
            return False

    def decrFreeChanCount(self):
        self.freeChannels = self.freeChannels - 1
        return

    def incrFreeChanCount(self):
        self.freeChannels = self.freeChannels + 1
        return

    def getShadowValues(self):
        return self._shadowValues
    
    def getSuccessCalls(self):
        return self.stats.successCalls
    
    def getEstblCalls(self):
        return self.stats.successCallEstablishment

    def printStats(self, time):
        print("+-------------------------------------------------------+------------------+")
        print("|        Statistics (BSTN - {0} after {1:d} Hrs )             |  Count           |".format(self._ID, time))
        print("+-------------------------------------------------------+------------------+")
        print("|")
        print("| NUMBER OF CHANNELS CURRENTLY IN USE = {0}".format(self._channels - self.freeChannels))
        print("|")
        
        self.stats.printStats()

        return

