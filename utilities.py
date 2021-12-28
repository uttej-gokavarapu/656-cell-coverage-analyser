###################################################################
# utilities.py
#  
# This python module contains the definitions of utility functions
#
# Author: @Uttej
# Date:   19th Nov 2021
#
# ENTS656 Python project
#
###################################################################

import numpy as np
import matplotlib.pyplot as plt


#-------------------------------------------------------------------
# Enums class for statistics names
#-------------------------------------------------------------------
import enum

class StatName(enum.Enum):
    CALL_ATTEMPTS                       = 0
    SUCCESSFUL_CALLS                    = 1
    SUCCESSFUL_CALL_ESTBL               = 2
    CALL_ESTBL_FAIL_DUE_SIGNAL_STRENGTH = 3
    HANDOFF_ATTEMPTS_OUT                = 4
    INCOMING_HANDOFF_RQTS               = 5
    SUCCESSFUL_HANDOFFS                 = 6
    HANDOFF_FAILURE                     = 7
    CALL_DROP_SIG_STRENGTH              = 8
    CALL_DROP_CAPACITY                  = 9
    CALL_BLOCK_CAPACITY                 = 10
    HANDOFF_RQTS_ACCEPTED               = 11
    HANDOFF_RQTS_REJECTED               = 12
    

#-------------------------------------------------------------------
# Okamura-Hata Model
#-------------------------------------------------------------------
def okamuraHata(d, f, Hb, Hm, corrFactor = 0):
    """ This function calculates the propagation loss based on Okamura-Hata Model
        
        Input:
          1. d - distance of mobile from base station (in KM)
          2. f - frequency in MHz
          3. Hb - height of base station from the ground (in meters)
          4. Hm - height of the mobile from the ground (in meters)
          5. corrFactor - Correction factor,
                          default value = 0 (Small or medium city)
                               if value = 1 (Sub urban)
                                  value = 2 (Rural)
                          #TODO: use enums to make the code more clean 

        Output: path loss based on Okamura-Hata propagation model in dB
    """

    A_Hm= (1.1*(np.log10(f)) - 0.7)*Hm - (1.56*(np.log10(f)) - 0.8)

    pL50 = 69.55 + 26.16*(np.log10(f)) - 13.82*(np.log10(Hb)) + (44.9 - 6.55*(np.log10(Hb)))*(np.log10(d)) - A_Hm 

    #Correction Factor computation:
    if corrFactor == 1:
        pL50 = pL50 - 2*((np.log10(f/28))**2) - 5.4

    elif corrFactor == 2:
        pL50 = pL50 - 4.78*((np.log10(f))**2) + 18.33*((np.log10(f))) - 40.95

    else:
        pass

    return pL50


#-------------------------------------------------------------------
# Shadowing
#-------------------------------------------------------------------
def shadowing(sampleSize, mean = 2, std = 2, seedVal = 0, useSeed = False):
    """ This function generates random samples of size 'sampleSize' from 
        gaussian distribution

        Input:
          1. sampleSize - Number of samples to be generated
          2. mean - mean of distribution (default value = 2)
          3. std  - Standard deviation of distribution (default value = 2) 
                    (Must be non negative value!!, if negative value is entered, default value will be used!)
          4. seedVal - seed value to be used to generate the shadowing array
          5. useSeed - boolean flag to say whether use the seed or not

        Output: Returns a numpy array of samples""" 
    
    #Sanity Check!
    if std < 0:
        std = 2 #using default value
    
    #As the shadowing values depends on surroundings, 
    #these values does not change with different simulation runs.
    #To make sure the shadowing values stays constant across the simulation executions,
    #setting a pre-defined seed to geneate same set of values all the time
    #This makes the executions comparable (for different input values in differnt simulations)
    if useSeed == True:
        np.random.seed(seedVal)
    
    #Generate samples
    samples = np.random.normal(mean, std, sampleSize)
       
    #Reset the effect of random seed (So that other random functions are not affected)
    if useSeed == True:
        np.random.seed()

    return samples


#-------------------------------------------------------------------
# Fading (using Rayleigh distribution)
#-------------------------------------------------------------------
def rayleighFading():
    
    """ This function generates two arrays of random samples. One for real and other 
        for imaginary part of size 10 using gaussian distribution with
        mean = zero and unit varience (which means std = 1). The magnitude is then 
        computed for generating complex gaussian distribution.

        Output: 
                Fading value in dB

        (To make the system survice the isolated deep fade, the second least value is 
        reported as the fading value)"""

    mean, std = 0.0, 1.0
    
    x = np.random.normal(mean, std, 10)
    y = np.random.normal(mean, std, 10)

    z = x + y*(1j)
    rayleigh = np.abs(z)

    #From the values obtained return the second least value
    rayleigh = np.sort(rayleigh)

    #The obtained value is linear and is voltage
    #To obtain power in dB, square the value and convert to decibles

    fadeInDB = 20 * (np.log10(rayleigh[1]))

    return fadeInDB


#-------------------------------------------------------------------
# Function to calculate EIRP in mobile direction
#-------------------------------------------------------------------
def calculateEIRP(EIRP_boreSight, tiltAngle, Hb, Hm, dstFromBstn, vertDiscrmData):

    """This function calculates the actual EIRP in the direction of mobile location.
       First, Calculates the vertical discrimination angle based on ths distances, 
       Then interpolates between the values in vertical_pattern.txt table

       Input:
         1. EIRP_boreSight - EIRP in the direction of bore sight.
         2. tiltAngle - Angle by which antenna is down tilted
         3. Hb - Height of base station (in meters)
         4. Hm - Height of mobile (in meters)
         5. dstFromBstn - Distance of the mobile from Base station (in meters)
         6. vertDiscrmData - a list containg float values of vertical discrimination values for angles 0 to 360

       Output:
               Returns the actual EIRP value in dB in the direction of mobile.   """
               
    #1. Compute angle between tip of the bstn to mobile
    gamma = np.rad2deg( np.arctan2((Hb - Hm), dstFromBstn) )

    #2. Calculate vertical angle discrimination and convert to positive value if negative
    beta = gamma - tiltAngle

    if beta < 0:
        beta += 360 

    #3. Based on the beta, compute vertical discrimination value
    #    a. If beta value is integer, then take the corresponding value from the array
    #    b. Else, interpolate between the values above and below

    x1 = int(np.floor(beta))
    x2 = int(np.ceil(beta))

    vertDiscrmtn = 0  #Initializing with zero

    if x1 == x2:  #integer
        vertDiscrmtn  = vertDiscrmData[x1]
    else:
        vertDiscrmtn = ( (beta - x1) * vertDiscrmData[x2] ) + ( (x2 - beta) * vertDiscrmData[x1] )

    #4. Now Compute the Actual EIRP in the direction of mobile
    actualEIRP = EIRP_boreSight - vertDiscrmtn


    return actualEIRP


#-------------------------------------------------------------------
# Function to read vertical discrimination data from file
#-------------------------------------------------------------------
def readVertDiscrmData(filepath):
    
    """ This function reads the data from filepath passed as an input argument and returms
        array of vertical discrimination values

        Input:
           filepath - The absolute path to the file containing vertical discrimination values.

        Output:
           A list of vertical discrimination values for 0 to 360 degrees  """

    vertDiscrmtnList = []

    with open(filepath, 'r') as fp:
        for line in fp:
            temp = (line.strip()).split()
            vertDiscrmtnList.append(float(temp[-1]))  #Append last value from the line

    #Adding entry for 360 degrees for the ease of computation
    temp = vertDiscrmtnList[0]
    vertDiscrmtnList.append(temp)

    return vertDiscrmtnList


#-----------------------------------------------------------------------
# Validate integer values function
#-----------------------------------------------------------------------
def validateInt(value, addnlCondition = 'all'):

    """ Validates integer values.
        
        Input:
            1. value - input to be validated.
            2. addnlCondition - all/positive/non-negative/negative (case insensitive)
                                This parameter can be extended with requirement. 
        Output: True/False  """
    
    #TODO: Add sanity check for addnlCondition input argument to check if entered value is string

    bRet = None #Intializing with None

    try:
        val = int(value)

        #Check additional conditions.
        addnlCondition = addnlCondition.lower()

        if addnlCondition == all:
            bRet = True
        elif addnlCondition == 'positive' and val > 0:
            bRet = True
        elif addnlCondition == 'non-negative' and val >= 0:
            bRet = True
        elif addnlCondition == 'negative' and val < 0:
            bRet = True
        else:
            bRet = False

    except ValueError:
        bRet = False

    return bRet


#-----------------------------------------------------------------------
# Validate float values function
#-----------------------------------------------------------------------
def validateFloat(value, addnlCondition = 'all'):

    """ Validates float values.
        
        Input:
            1. value - input to be validated.
            2. addnlCondition - all/positive/non-negative/negative (case insensitive)
                                This parameter can be extended with requirement. 
        Output: True/False  """
    
    #TODO: Add sanity check for addnlCondition input argument to check if entered value is string

    bRet = None #Intializing with None

    try:
        val = float(value)

        #Check additional conditions.
        addnlCondition = addnlCondition.lower()

        if addnlCondition == all:
            bRet = True
        elif addnlCondition == 'positive' and val > 0:
            bRet = True
        elif addnlCondition == 'non-negative' and val >= 0:
            bRet = True
        elif addnlCondition == 'negative' and val < 0:
            bRet = True
        else:
            bRet = False

    except ValueError:
        bRet = False

    return bRet

#------------------------------------------------------------------
# Function to plot S/I values as bar graph
#------------------------------------------------------------------
def plotSgnlIxInfo(data, roadLen):
    """ This function takes the S/I values obtained at differnt locations 
        during the call time. Counts the number of points which have
               S/I >= 10dB
               10dB > S/I >= 5dB
               S/i < 5dB     for each base station, 
        and plots a bar graph to classify each section of road block

        Input: 
            1. data - list of tuples [(location, serving base station, S/I value)]
            2. roadLen - length of road in meters

        Output:
            Plots seperate bar graphs for each base station. """

    ROAD_SECTION_SIZE = 100
    
    #Maintain a lists of lists for each base station in a dictionary
    #           [ [count of S/I > 10dB in a section],
    #             [count of 5dB < S/I < 10 dB],
    #             [count of S/I > 10dB] ]
    
    totalRoadSections = roadLen//ROAD_SECTION_SIZE

    dictSgnlIx = {'A': [[0]*totalRoadSections, [0]*totalRoadSections, [0]*totalRoadSections] , \
                  'B': [[0]*totalRoadSections, [0]*totalRoadSections, [0]*totalRoadSections] }
    

    for tupval in data:
        #1. check the location and determine to which block it belongs to..
        locationIndex = int(np.floor(tupval[0]/ROAD_SECTION_SIZE))
       
        #2. identify serving base station
        servingBstn = tupval[1]

        #2. determine the category of S/I value
        sgnlIxRatio = tupval[2]

        if sgnlIxRatio > 10:
            dictSgnlIx[servingBstn][2][locationIndex] += 1
        
        elif sgnlIxRatio > 5:
            dictSgnlIx[servingBstn][1][locationIndex] += 1

        else:
            dictSgnlIx[servingBstn][0][locationIndex] += 1


    #Now plot the bar graph for each base station
    barWidth = 25
    xaxis = np.arange(100, roadLen+100, 100)
    
    plt.figure(0, figsize=(20, 10))
    plt.bar(xaxis, dictSgnlIx['A'][0], barWidth, label='< 5dB', color='r')
    plt.bar(xaxis+barWidth, dictSgnlIx['A'][1], barWidth, label='> 5dB and < 10dB', color='m')
    plt.bar(xaxis+2*barWidth, dictSgnlIx['A'][2], barWidth, label='> 10dB', color='g')
    plt.xticks(np.arange(0, 6001, 100),rotation = -45)
    plt.xlabel('distances on road (left to right)')
    plt.ylabel('Count')
    plt.title('S/I bar chart for BASE STATION-A')
    plt.legend(loc='best', prop={'size': 20})

    plt.figure(1, figsize=(20, 10))
    plt.bar(xaxis, dictSgnlIx['B'][0], barWidth, label='< 5dB', color='r')
    plt.bar(xaxis+barWidth, dictSgnlIx['B'][1], barWidth, label='> 5dB and < 10dB', color='m')
    plt.bar(xaxis+2*barWidth, dictSgnlIx['B'][2], barWidth, label='> 10dB', color='g')
    plt.xticks(np.arange(0, 6001, 100),rotation = -45)
    plt.xlabel('distances on road (left to right)')
    plt.ylabel('Count')
    plt.title('S/I bar chart for BASE STATION-B')
    plt.legend(loc='best', prop={'size': 20})

    plt.show()
    
    return

