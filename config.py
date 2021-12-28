###################################################################
# config.py
#  
# This python file contains all the configurations for the project
#
# Author: @Uttej
# Date:   20th Nov 2021
#
# ENTS656 Python project
#
###################################################################


#------------------------------------------------------------------
# ** GENERAL PARAMETERS **
#------------------------------------------------------------------
ROAD_LENGTH              = 6000  # In meters
SIMULATION_STEP_SIZE     = 1     # seconds
VERTICAL_PATTERN_FILEPATH = './vertical_pattern.txt'


#------------------------------------------------------------------
# ** BASE-STATION PARAMETERS **
#------------------------------------------------------------------
BSTN_HEIGHT              = 50    # In meters
BSTN_LOCATION            = 15    # In meters orthogonal to road
TX_POWER                 = 43    # In dBm
CONNECTOR_LOSSES         = 1     # In dB
ANTENNA_GAIN             = 14.8  # In dB
CHANNELS_PER_SECTOR      = 15
FREQUENCY                = 800   # In MHz

#------------------------------------------------------------------
# ** MOBILE/USER PARAMETERS **
#------------------------------------------------------------------
MOBILE_HEIGHT            = 1     # In meters
HANDOFF_MARGIN           = 3     # In dB
RX_THRESHOLD             = -100  # In dBm
CALL_RATE                = 2     # Calls per hour (on average)
AVG_CALL_DURATION        = 180   # seconds/call

MOBILE_SPEED_MEAN        = 12    # In meter/sec
MOBILE_SPEED_STD         = 3     # In meter/sec


#------------------------------------------------------------------
# ** SHADOWING PARAMETERS **
#------------------------------------------------------------------
SHADOWING_RESOLUTION     = 20    # In meters
SHADOWING_MEAN           = 2     # In dB
SHADOWING_STD            = 2     # In dB


