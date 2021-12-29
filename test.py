###################################################################
# script_part1.py
#  
# This python script contains the definitions of utility functions
# And uses them to compute RSL values
#
# Author: @Uttej
# Date:   19th Nov 2021
#
# ENTS656 Python project - part1
#
###################################################################

import numpy as np
import matplotlib.pyplot as plt
import utilities as util


# ** GENERAL PARAMETERS **

ROAD_LENGTH              = 6000  # In meters
VERTICAL_PATTERN_FILEPATH = './vertical_pattern.txt'

BSTN_HEIGHT              = 50    # In meters
BSTN_LOCATION            = 15    # In meters orthogonal to road
TX_POWER                 = 43    # In dBm
CONNECTOR_LOSSES         = 1     # In dB
ANTENNA_GAIN             = 14.8  # In dB
FREQUENCY                = 800   # In MHz

MOBILE_HEIGHT            = 1     # In meters
SHADOWING_RESOLUTION     = 20    # In meters


#1. Read vertical_pattern.txt file and store the discrimination values.
vertDiscrmnData = util.readVertDiscrmData(VERTICAL_PATTERN_FILEPATH)

#2. Calculate the EIRP bore sight
EIRP_BORE_SIGHT = TX_POWER - CONNECTOR_LOSSES + ANTENNA_GAIN

#3. Compute Shadowing values
shadowBstnA = util.shadowing(ROAD_LENGTH//SHADOWING_RESOLUTION)
shadowBstnB = util.shadowing(ROAD_LENGTH//SHADOWING_RESOLUTION)

#4. Initialize the distance array (positioning from left to right [BSTN-A to BSTN-B])
distances = np.linspace(0, 6000, 6001)


##------------------------ ** BASE STATION A ** ------------------------------

actualDstFromBstnA = np.sqrt( (BSTN_LOCATION ** 2)  + (distances ** 2) )

# a. Calculate the propagation loss (gives the array of Propagation loss for each distance)
pLossbstnA = util.okamuraHata(actualDstFromBstnA/1000, FREQUENCY, BSTN_HEIGHT, MOBILE_HEIGHT)

# b. Calculate EIRP in mobile direction with different tilt values
eirpTilt0_bstnA = []
eirpTilt2_bstnA = []
eirpTilt5_bstnA = []
eirpTilt10_bstnA = []

for distance in list(actualDstFromBstnA):
    
    temp  = util.calculateEIRP(EIRP_BORE_SIGHT, 0, BSTN_HEIGHT, MOBILE_HEIGHT, distance, vertDiscrmnData)
    eirpTilt0_bstnA.append(temp)
    
    temp = util.calculateEIRP(EIRP_BORE_SIGHT, 2, BSTN_HEIGHT, MOBILE_HEIGHT, distance, vertDiscrmnData)
    eirpTilt2_bstnA.append(temp)
    
    temp = util.calculateEIRP(EIRP_BORE_SIGHT, 5, BSTN_HEIGHT, MOBILE_HEIGHT, distance, vertDiscrmnData)
    eirpTilt5_bstnA.append(temp)
    
    temp = util.calculateEIRP(EIRP_BORE_SIGHT, 10, BSTN_HEIGHT, MOBILE_HEIGHT, distance, vertDiscrmnData)
    eirpTilt10_bstnA.append(temp)


# ** Plot the Graphs **
plt.figure(0)

#1. EIRP bore sight - propagation loss
rslBoreSight_bstnA = EIRP_BORE_SIGHT - pLossbstnA
plt.plot(distances, rslBoreSight_bstnA, label='RSL Boresight')

#2. (EIRP direction of mobile with tilt=0) - propagation loss
rslTilt0_bstnA = np.array(eirpTilt0_bstnA) - pLossbstnA
plt.plot(distances, rslTilt0_bstnA, label='RSL with tilt = 0')

#3. (EIRP direction of mobile with tilt=2) - propagation loss
rslTilt2_bstnA = np.array(eirpTilt2_bstnA) - pLossbstnA
plt.plot(distances, rslTilt2_bstnA, label='RSL with tilt = 2')

#4. (EIRP direction of mobile with tilt=5) - propagation loss
rslTilt5_bstnA = np.array(eirpTilt5_bstnA) - pLossbstnA
plt.plot(distances, rslTilt5_bstnA, label='RSL with tilt = 5')

#5. (EIRP direction of mobile with tilt=10) - propagation loss
rslTilt10_bstnA = np.array(eirpTilt10_bstnA) - pLossbstnA
plt.plot(distances, rslTilt10_bstnA, label='RSL with tilt = 10')

plt.xlabel('Position of mobile on road (Left to right) in meters')
plt.ylabel('RSL in dBm')
plt.title('RSL values for bstnA with different tilt values')
plt.grid(linestyle='dotted')
plt.legend(loc='upper right')



##------------------------ ** BASE STATION B ** ------------------------------

actualDstFromBstnB = np.sqrt( (BSTN_LOCATION ** 2)  + ((ROAD_LENGTH - distances) ** 2) )

# a. Calculate the propagation loss (gives the array of Propagation loss for each distance)
pLossbstnB = util.okamuraHata(actualDstFromBstnB/1000, FREQUENCY, BSTN_HEIGHT, MOBILE_HEIGHT)

# b. Calculate EIRP in mobile direction with different tilt values
eirpTilt0_bstnB = []
eirpTilt2_bstnB = []
eirpTilt5_bstnB = []
eirpTilt10_bstnB = []

for distance in list(actualDstFromBstnB):
    
    temp = util.calculateEIRP(EIRP_BORE_SIGHT, 0, BSTN_HEIGHT, MOBILE_HEIGHT, distance, vertDiscrmnData)
    eirpTilt0_bstnB.append(temp)
    
    temp = util.calculateEIRP(EIRP_BORE_SIGHT, 2, BSTN_HEIGHT, MOBILE_HEIGHT, distance, vertDiscrmnData)
    eirpTilt2_bstnB.append(temp)
    
    temp = util.calculateEIRP(EIRP_BORE_SIGHT, 5, BSTN_HEIGHT, MOBILE_HEIGHT, distance, vertDiscrmnData)
    eirpTilt5_bstnB.append(temp)
    
    temp = util.calculateEIRP(EIRP_BORE_SIGHT, 10, BSTN_HEIGHT, MOBILE_HEIGHT, distance, vertDiscrmnData)
    eirpTilt10_bstnB.append(temp)


#Plot the Graphs
plt.figure(1)

#1. EIRP bore sight - propagation loss
rslBoreSight_bstnB = EIRP_BORE_SIGHT - pLossbstnB
plt.plot(distances, rslBoreSight_bstnB, label='RSL Boresight')

#2. (EIRP direction of mobile with tilt=0) - propagation loss
rslTilt0_bstnB = np.array(eirpTilt0_bstnB) - pLossbstnB
plt.plot(distances, rslTilt0_bstnB, label='RSL with tilt = 0')

#3. (EIRP direction of mobile with tilt=2) - propagation loss
rslTilt2_bstnB = np.array(eirpTilt2_bstnB) - pLossbstnB
plt.plot(distances, rslTilt2_bstnB, label='RSL with tilt = 2')

#4. (EIRP direction of mobile with tilt=5) - propagation loss
rslTilt5_bstnB = np.array(eirpTilt5_bstnB) - pLossbstnB
plt.plot(distances, rslTilt5_bstnB, label='RSL with tilt = 5')

#5. (EIRP direction of mobile with tilt=10) - propagation loss
rslTilt10_bstnB = np.array(eirpTilt10_bstnB) - pLossbstnB
plt.plot(distances, rslTilt10_bstnB, label='RSL with tilt = 10')


plt.xlabel('Position of mobile on road (Left to right) in meters')
plt.ylabel('RSL in dBm')
plt.title('RSL values for bstnB with different tilt values')
plt.grid(linestyle='dotted')
plt.legend(loc='upper center')


##--------------------------------------------------------------------------------------------
# ** Calculate RSL with fading and shadowing for tilt = 2  for base station A  and B **
##--------------------------------------------------------------------------------------------

rslShadowFade_bstnA = []
rslShadowFade_bstnB = []

for count in range(len(distances)):
    
    #First compute for base station A
    shadowIndex_bstnA = int(distances[count]//SHADOWING_RESOLUTION)
    
    #This happens when distance = 6000, then take the value of shadow from last index
    if shadowIndex_bstnA == len(shadowBstnA):
        shadowIndex_bstnA = shadowIndex_bstnA - 1
    
    temp = rslTilt2_bstnA[count] + shadowBstnA[shadowIndex_bstnA] + util.rayleighFading()
        
    rslShadowFade_bstnA.append(temp)
    
    #Now compute for base station B
    shadowIndex_bstnB = int((ROAD_LENGTH - distances[count])//SHADOWING_RESOLUTION)
    
    #This happens when distance = 6000, then take the value of shadow from last index
    if shadowIndex_bstnB == len(shadowBstnB):
        shadowIndex_bstnB = shadowIndex_bstnB - 1
    
    temp = rslTilt2_bstnB[count] + shadowBstnB[shadowIndex_bstnB] + util.rayleighFading()
        
    rslShadowFade_bstnB.append(temp)


#Plot the graphs
plt.figure(2)

plt.plot(distances, np.array(rslShadowFade_bstnA), 'b', label='RSL for bstn A with shadowing and fading')
plt.plot(distances, rslTilt2_bstnA, 'w--',  label='RSL for bstn A w/o shadowing and fading')
plt.plot(distances, np.array(rslShadowFade_bstnB), 'r', label='RSL for bstn B with shadowing and fading')
plt.plot(distances, rslTilt2_bstnB, 'k--', label='RSL for bstn B w/o shadowing and fading')

plt.xlabel('Position of mobile on road (Left to right) in meters')
plt.ylabel('RSL in dBm')
plt.title('RSL values for antenna tilt = 2 degrees')
plt.grid(linestyle='dotted')
plt.legend(loc='upper center')

plt.show()
