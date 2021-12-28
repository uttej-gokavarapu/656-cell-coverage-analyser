###################################################################
# main.py
#  
# This python script is starting point of the simulation. Performs 
# the tasks required for thr project
#
# Author: @Uttej
# Date:   20th Nov 2021
#
# ENTS656 Python project
#
###################################################################


#------------------------------------------------------------------
# Import statements
#------------------------------------------------------------------
import utilities as util
import basestation as bstn
import mobile as mobile
import callManagement as callMngt
import config as cfg
import numpy as np


#------------------------------------------------------------------
# Simulation execution starts from here!!
#------------------------------------------------------------------

#------------------------------
# ** TAKE USER INPUTS **
#------------------------------

numOfUsers  = 0   # Total number of users
tilt        = 0   # Antenna tilt
tTotal      = 0   # Total simulation time

# Get Number of users
while True:
    temp  = input('Enter number of users: ')

    if util.validateInt(temp, 'positive'):
        numOfUsers = int(temp)
        break
    else:
        print('Invalid value.. Please enter positive integer values!')

# Get Antenna tilt angle
while True:
    temp  = input('Enter Antenna tilt (in degrees): ')

    if util.validateFloat(temp, 'non-negative'):
        tilt = float(temp)
        break
    else:
        print('Invalid value.. Please enter non negative float values!')

# Get Total simulation time
while True:
    temp  = input('Enter Total simulation time (in Hrs): ')

    if util.validateFloat(temp, 'positive'):
        tTotal = float(temp)

        #Convert Hrs to sec
        tTotal = int(tTotal*3600)

        break
    else:
        print('Invalid value.. Please enter positive float values!')

#------------------------------
# ** Intialize settings ** 
#------------------------------

#1. Read vertical_pattern.txt file and store the discrimination values.
vertDiscrmnData = util.readVertDiscrmData(cfg.VERTICAL_PATTERN_FILEPATH)

#2. Compute Shadowing values
shadowBstnA = util.shadowing(cfg.ROAD_LENGTH//cfg.SHADOWING_RESOLUTION, cfg.SHADOWING_MEAN, cfg.SHADOWING_STD, 0, True)
shadowBstnB = util.shadowing(cfg.ROAD_LENGTH//cfg.SHADOWING_RESOLUTION, cfg.SHADOWING_MEAN, cfg.SHADOWING_STD, 4, True)

#3. Instatiate the base station objects (EIRP bore sight calculation is done inside constructor) 
bstnDataBase = {}
bstnDataBase['A'] = bstn.BaseStation('A', cfg.BSTN_HEIGHT, cfg.BSTN_LOCATION, cfg.TX_POWER, \
                                     cfg.CONNECTOR_LOSSES, cfg.ANTENNA_GAIN, \
                                     cfg.CHANNELS_PER_SECTOR, cfg.FREQUENCY, tilt, vertDiscrmnData, shadowBstnA)

bstnDataBase['B'] = bstn.BaseStation('B', cfg.BSTN_HEIGHT, cfg.BSTN_LOCATION, cfg.TX_POWER, \
                                     cfg.CONNECTOR_LOSSES, cfg.ANTENNA_GAIN, \
                                     cfg.CHANNELS_PER_SECTOR, cfg.FREQUENCY, tilt, vertDiscrmnData, shadowBstnB)

#4. Instatiate user object
#Maintain a dictionary of user objects with key as ID and value as object
userDataBase = {}  

#5. Now similarly maintain a dictionary of active, archive and inactive user id for tracking purpose
userIdDataBase = {'Active':[], 'Archived':[], 'Inactive':[]}

#6. Create mobile objects
for iCount in range(numOfUsers):
    temp = mobile.Mobile(iCount+1, cfg.MOBILE_HEIGHT, cfg.HANDOFF_MARGIN, cfg.RX_THRESHOLD)
    userDataBase[iCount+1] = temp
    userIdDataBase['Inactive'].append(iCount+1)  #Add the mobile id to inactive list

#7. Maintain a list to store the S/I values
#This list will hold tuples (location, serving bstn, S/I value)
sgnlToIxList = []


#---------------------------------------------------
# ** START SIMULATION **
#---------------------------------------------------
for count in range((tTotal//cfg.SIMULATION_STEP_SIZE)+1):
#{ Start of for loop
    
    #1. Loop through active users
    for userId in userIdDataBase['Active']:
    #{ Start of for loop
        user = userDataBase[userId]

        #Update the info of user (updates new location and checks if call is complete)
        bRet = callMngt.updateUserCallInfo(user, cfg.SIMULATION_STEP_SIZE)
        
        if bRet:
            #This means call is sucessfully completed, increment stat 
            bstnConnected = bstnDataBase[user.getConnectedBstnID()]
            
            bstnConnected.stats.incrStat(util.StatName.SUCCESSFUL_CALLS)
            bstnConnected.incrFreeChanCount()
            user.reset()

            #move the user from active list to archive list
            #Note: Here only adding the id to archived list but not removing it from active list, 
            #My Thumb rule: Never directly remove an element from the data structure we are looping through. 
            #If we do then it will lead to crash. (but not sure about python!!)
            userIdDataBase['Archived'].append(userId)
        else:
        #{ Start of else
            
            #1. Calculate the RSL at new location from both base stations
            bstnServer = bstnDataBase[user.getConnectedBstnID()]
            rslServer = callMngt.findRSL(user, bstnServer)

            if rslServer < user.getRxThreshold():
                #Drop the call
                bstnServer.stats.incrStat(util.StatName.CALL_DROP_SIG_STRENGTH)
                bstnServer.incrFreeChanCount()
                user.reset()

                #move the user to archive list
                userIdDataBase['Archived'].append(userId)

            else:
            #{ Start of else
                otherBstnId = 'B'
                if user.getConnectedBstnID() == 'B':
                    otherBstnId = 'A'

                bstnOther = bstnDataBase[otherBstnId]
                rslOther = callMngt.findRSL(user, bstnOther)

                #Push S/I tuple to global list.....
                sgnlIxTuple = (user.getPosition(), user.getConnectedBstnID(), rslServer - rslOther)
                sgnlToIxList.append(sgnlIxTuple)

                if rslOther > rslServer + user.getHandOffMargin():
                    bstnServer.stats.incrStat(util.StatName.HANDOFF_ATTEMPTS_OUT)
                    bstnOther.stats.incrStat(util.StatName.INCOMING_HANDOFF_RQTS)

                    if bstnOther.isFreeChanAvailable():
                        user.setConnectedBstnID(otherBstnId)   #Changing serving bstn
                        bstnOther.decrFreeChanCount()
                        bstnServer.incrFreeChanCount()

                        #Increment successful handoff out stat for old bstn
                        bstnServer.stats.incrStat(util.StatName.SUCCESSFUL_HANDOFFS)
                        bstnOther.stats.incrStat(util.StatName.HANDOFF_RQTS_ACCEPTED)

                    else:
                        #Increment handoff failed stat for serving bstn
                        bstnServer.stats.incrStat(util.StatName.HANDOFF_FAILURE)
                        bstnOther.stats.incrStat(util.StatName.HANDOFF_RQTS_REJECTED)
         
            #}End of else
         #}End of else
    #}End of for loop..

    #remove the archived users from active list before going to address inactive users
    userIdDataBase['Active'] = [elem for elem in userIdDataBase['Active'] if elem not in userIdDataBase['Archived']]

    #2. We are done dealing with active users. Now, loop through inactive users
    tempActiveList = []

    for userId in userIdDataBase['Inactive']:
    #{ Start of for loop    
        user = userDataBase[userId]

        #Determine if the user makes a call
        probability = (cfg.CALL_RATE/3600) * cfg.SIMULATION_STEP_SIZE

        #If user is making a call request
        if np.random.uniform() < probability:
        #{ start of if
            #1. Determine user's location
            location = np.random.uniform(0, cfg.ROAD_LENGTH)
            user.setPosition(location)

            #2. Set Direction
            if location > cfg.ROAD_LENGTH/2:
                user.setDirection(-1) #-1 means right to left
            else:
                user.setDirection(1)  #+1 means left to right

            #3. Find RSL at mobile from both Bstns
            rslA = callMngt.findRSL(user, bstnDataBase['A'])
            rslB = callMngt.findRSL(user, bstnDataBase['B'])

            rslServer = rslA   #Initialize higher value as A
            rslOther = rslB
            serverBstn = bstnDataBase['A']
            otherBstn = bstnDataBase['B']

            if rslB > rslA:
                rslServer = rslB
                rslOther = rslA
                serverBstn = bstnDataBase['B']
                otherBstn = bstnDataBase['A']

            #4. Check if the RSL server is greater than mobile threshold
            if rslServer < user.getRxThreshold():
                #Increment call drop stat for server bstn
                serverBstn.stats.incrStat(util.StatName.CALL_ESTBL_FAIL_DUE_SIGNAL_STRENGTH)
            
            else:
            #{ start of else
                #Attempt to establish a call, increment stat
                serverBstn.stats.incrStat(util.StatName.CALL_ATTEMPTS)

                if serverBstn.isFreeChanAvailable():
                    callMngt.establishCall(user, serverBstn)   #establish the call
                    tempActiveList.append(userId)     #Add user to active call list

                else:
                    #1.Increment the call blocked due to capacity stat for serving base station
                    serverBstn.stats.incrStat(util.StatName.CALL_BLOCK_CAPACITY)

                    #2. Check if the other bstn can take up the call
                    if rslOther > user.getRxThreshold() and otherBstn.isFreeChanAvailable():
                        otherBstn.stats.incrStat(util.StatName.CALL_ATTEMPTS)
                        callMngt.establishCall(user, otherBstn)    #establish the call
                        tempActiveList.append(userId)  #Add user to active call list

                    else:
                        #increment the dropped call due to cap stat for ORIGINAL bstn
                        serverBstn.stats.incrStat(util.StatName.CALL_DROP_CAPACITY)

            #} End of else
        #} End of if
    #} End of for loop..    
    
    #3. Adding the temp active user ids to Active list
    userIdDataBase['Active'].extend(tempActiveList)

    #removing the new active users from inactive list
    userIdDataBase['Inactive'] = [elem for elem in userIdDataBase['Inactive'] if elem not in tempActiveList]

    #4. we are done dealing with both active and inactive user at this time stamp
    #Move the archived users to inactive pool
    userIdDataBase['Inactive'].extend(userIdDataBase['Archived'])
    userIdDataBase['Archived'] = []  #Empty the list

    #5. Check the timer and print stats after every hour
    if count > 0 and count%3600 == 0:
        bstnDataBase['A'].printStats(count//3600)
        print('\n\n')
        bstnDataBase['B'].printStats(count//3600)
        print('\n-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-\n')

#} End of simulation timer For loop

# Now plot S/I bar graph
util.plotSgnlIxInfo(sgnlToIxList, cfg.ROAD_LENGTH)
