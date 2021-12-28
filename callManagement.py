###################################################################
# callManagement.py
#  
# This python module contains the function definitions of call 
# management
#
# Author: @Uttej
# Date:   20th Nov 2021
#
# ENTS656 Python project
#
###################################################################

import utilities as util
import config as cfg
import numpy as np


#------------------------------------------------------------------
# Function for Calculating RSL 
#------------------------------------------------------------------
def findRSL(mobl, bstn):
    """ This function takes mobile and bstn objects as input and 
        calculates the RSL value at mobile from the base station

        Input:
            1. mobl - mobile to which RSL is calculated
            2. bstn - base station from which RSL is calculated

        Output:
            RSL value in (dBm)  """

    moblPosition = mobl.getPosition()
    bstnID = bstn.getID()
    bstnLocation = bstn.getLocation()

    #Calculate the distance between mobile & bstn based on the position and bstn ID
    dstFromBstn = moblPosition

    if bstnID == 'B':
        dstFromBstn = cfg.ROAD_LENGTH - moblPosition

    actualDstFromBstn = np.sqrt( (bstnLocation ** 2)  + (dstFromBstn ** 2) )
    #actualDstFromBstn = dstFromBstn

    eirp = util.calculateEIRP(bstn.getBoreSightEIRP(), bstn.getTilt(), \
                              bstn.getHeight(), mobl.getHeight(), \
                              actualDstFromBstn, bstn.getVertDiscrmnData())

    pLoss = util.okamuraHata(actualDstFromBstn/1000, bstn.getOperationalFreq(), \
                             bstn.getHeight(), mobl.getHeight())

    shadowValues = bstn.getShadowValues()

    shadowIndex = int(dstFromBstn//cfg.SHADOWING_RESOLUTION)

    #This happens when distance is exactly 6000, then take the value of shadow from last index
    if shadowIndex >= len(shadowValues):
        shadowIndex = len(shadowValues) - 1
    
    shadow = shadowValues[shadowIndex]

    fade = util.rayleighFading()

    #Compute RSL
    rsl = eirp - pLoss + shadow + fade

    return rsl

#------------------------------------------------------------------
# Function to establish call 
#------------------------------------------------------------------
def establishCall(user, bstn):
    """ This function takes care of the actions required to establish call.
        Determines the length of the call duration, Speed of the user etc 
        and saves the information in the user 

        Input:
            1. user - mobile object for which call is getting established
            2. bstn - base station to which the boile is getting connected"""
    
    #1. Determine length of the call
    duration = np.random.exponential(cfg.AVG_CALL_DURATION) # value passed in is 180sec
    user.setCallDurationLeft(duration)

    #2. Determine the speed of the user
    speed = np.random.normal(cfg.MOBILE_SPEED_MEAN, cfg.MOBILE_SPEED_STD)
    user.setSpeed(speed)

    #3. Set the bstn ID as serving base station in mobile object
    user.setConnectedBstnID(bstn.getID())

    #4. Decrement number of free channels on base station
    bstn.decrFreeChanCount()

    #5. Increment the stat, Successful call establishments
    bstn.stats.incrStat(util.StatName.SUCCESSFUL_CALL_ESTBL)

    return

#------------------------------------------------------------------
# Function to update user info
#------------------------------------------------------------------
def updateUserCallInfo(user, delta_T):
    """ This fuction calculates updates the user information such as position on the road, 
        call duration etc.. This function returns 'True' is a call is successfully completed
        else returns 'False'

        Input: 
            1. user - mobile object on which infomation is being changes
            2. delta_T - time difference
        
        Output:
            True - Call successfully completed
            False - Call is still going on!!"""

    #1. update user's location (either +1 pr -1)
    direction = user.getDirection()
    speed = user.getSpeed()
    currentLoctn = user.getPosition()

    # New location = current Location (+ or -) distance travelled
    newLocation = currentLoctn + (direction) * (speed * delta_T)

    #2. Change the call duration left
    currentDurLeft = user.getCallDurationLeft()

    newDurLeft = currentDurLeft - delta_T

    bRet = False #Initializing that call is not terminated

    if newDurLeft <= 0 or (newLocation >= 6000 or newLocation <= 0):
        bRet = True
    else:
        user.setCallDurationLeft(newDurLeft)
        user.setPosition(newLocation)

    return bRet


