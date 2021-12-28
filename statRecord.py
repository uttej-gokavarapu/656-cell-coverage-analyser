###################################################################
# statistics.py
#  
# This python module contains the declaration and definition of 
# Statistics class and its methods
#
# Author: @Uttej
# Date:   22nd Nov 2021
#
# ENTS656 Python project
#
###################################################################
from utilities import StatName

class Statistics:

    def __init__(self):

        #initialize all the statistics to zero
        self.callAttempts               =  0
        self.successCallEstablishment   =  0
        self.callEstblFailDueSignlStrnt =  0
        self.successCalls               =  0
        self.successHandoffs            =  0
        self.handoffsFailed             =  0
        self.handoffsIn                 =  0
        self.handoffsOut                =  0
        self.callDropDueSgnlStrength    =  0
        self.callDropDueCapacity        =  0
        self.blockDueCapacity           =  0
        self.handoffInSuccess           =  0
        self.handoffInFail              =  0


    def incrStat(self, statName):

        if statName == StatName.CALL_ATTEMPTS:
            self.callAttempts += 1
        elif statName == StatName.SUCCESSFUL_CALLS:
            self.successCalls += 1
        elif statName == StatName.SUCCESSFUL_CALL_ESTBL:
            self.successCallEstablishment += 1
        elif statName == StatName.CALL_ESTBL_FAIL_DUE_SIGNAL_STRENGTH:
            self.callEstblFailDueSignlStrnt += 1
        elif statName == StatName.SUCCESSFUL_HANDOFFS:
            self.successHandoffs += 1
        elif statName == StatName.HANDOFF_FAILURE:
            self.handoffsFailed += 1
        elif statName == StatName.HANDOFF_ATTEMPTS_OUT:
            self.handoffsOut += 1
        elif statName == StatName.INCOMING_HANDOFF_RQTS:
            self.handoffsIn += 1
        elif statName == StatName.CALL_DROP_SIG_STRENGTH:
            self.callDropDueSgnlStrength += 1  
        elif statName == StatName.CALL_DROP_CAPACITY:
            self.callDropDueCapacity += 1
        elif statName == StatName.CALL_BLOCK_CAPACITY:
            self.blockDueCapacity += 1
        elif statName == StatName.HANDOFF_RQTS_ACCEPTED:
            self.handoffInSuccess += 1
        elif statName == StatName.HANDOFF_RQTS_REJECTED:
            self.handoffInFail += 1
        
        return


    def decrStat(self, statName):

        if statName == StatName.CALL_ATTEMPTS:
            self.callAttempts -= 1
        elif statName == StatName.SUCCESSFUL_CALLS:
            self.successCalls -= 1
        elif statName == StatName.SUCCESSFUL_CALL_ESTBL:
            self.successCallEstablishment -= 1
        elif statName == StatName.CALL_ESTBL_FAIL_DUE_SIGNAL_STRENGTH:
            self.callEstblFailDueSignlStrnt -= 1
        elif statName == StatName.SUCCESSFUL_HANDOFFS:
            self.successHandoffs -= 1
        elif statName == StatName.HANDOFF_FAILURE:
            self.handoffsFailed += 1
        elif statName == StatName.HANDOFF_ATTEMPTS_OUT:
            self.handoffsOut -= 1
        elif statName == StatName.INCOMING_HANDOFF_RQTS:
            self.handoffsIn -= 1
        elif statName == StatName.CALL_DROP_SIG_STRENGTH:
            self.callDropDueSgnlStrength -= 1  
        elif statName == StatName.CALL_DROP_CAPACITY:
            self.callDropDueCapacity -= 1
        elif statName == StatName.CALL_BLOCK_CAPACITY:
            self.blockDueCapacity -= 1
        elif statName == StatName.HANDOFF_RQTS_ACCEPTED:
            self.handoffInSuccess -= 1
        elif statName == StatName.HANDOFF_RQTS_REJECTED:
            self.handoffInFail -= 1

        return


    def printStats(self):

        print("|  CALL STATISTICS: ")
        print("|   +---------------------------------------------------+---------------+   ")
        print("|   | Number of Call Attempts                           | \t{0}".format(self.callAttempts))
        print("|   +---------------------------------------------------+---------------+   ")
        print("|   | Number of Call Establishments success             | \t{0}".format(self.successCallEstablishment))
        print("|   +---------------------------------------------------+---------------+   ")
        print("|   | Number of Call Establish fail due signal strength | \t{0}".format(self.callEstblFailDueSignlStrnt))
        print("|   +---------------------------------------------------+---------------+   ")
        print("|   | Number of Call Blocks due capacity                | \t{0}".format(self.blockDueCapacity))
        print("|   +---------------------------------------------------+---------------+   ")
        print("|   | Number of Successful Calls                        | \t{0}".format(self.successCalls))
        print("|   +---------------------------------------------------+---------------+   ")
        print("|   | Number of Call drops due Sgnl strength            | \t{0}".format(self.callDropDueSgnlStrength))
        print("|   +---------------------------------------------------+---------------+   ")
        print("|   | Number of Call drops due Capacity                 | \t{0}".format(self.callDropDueCapacity))
        print("|   +---------------------------------------------------+---------------+   ")
        print("|")
        print("| HANDOFF STATISTICS: ")
        print("|   +---------------------------------------------------+---------------+   ")
        print("|   | Number of Handoffs Attempts outside bstn          | \t{0}".format(self.handoffsOut))
        print("|   +---------------------------------------------------+---------------+   ")
        print("|   | Number of Successful Handoffs outside             | \t{0}".format(self.successHandoffs))
        print("|   +---------------------------------------------------+---------------+   ")
        print("|   | Number of Handoffs Failed                         | \t{0}".format(self.handoffsFailed))
        print("|   +---------------------------------------------------+---------------+   ")
        print("|   | Number of Incoming Handoff requests               | \t{0}".format(self.handoffsIn))
        print("|   +---------------------------------------------------+---------------+   ")
        print("|   | Number of Incoming Handoff requests Accepted      | \t{0}".format(self.handoffInSuccess))
        print("|   +---------------------------------------------------+---------------+   ")
        print("|   | Number of Incoming Handoff requests Rejected      | \t{0}".format(self.handoffInFail))
        print("|   +---------------------------------------------------+---------------+   ")
        print("|")
        print("+-------------------------------------------------------+------------------+")


        return

