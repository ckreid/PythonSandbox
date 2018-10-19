'''
Created on Oct 17, 2018

@author: clayton.reid
'''

import os
import sys
import time

import DataManager

from Common import Common, CommonLogging

import logging
log = logging.getLogger( __name__ )

def basicDataDump():
    sFilepath = os.path.join( Common.sCurrentDirectory, "InputScores" )
    dataManager = DataManager.GameEndDataManager( sFilepath )
    if dataManager.m_bIsValid:
        print( "Average Game Interest: {}".format( dataManager.getAverageGameInterest() ) )
        print( dataManager.printAllInterestsPerGame() )
        print( "\nAverage Interest per Faction\n{}".format( dataManager.printAllFactionAverageInterests() ) )
        print( "\nAverage Game Interest per Faction\n{}".format( dataManager.printAllFactionAverageGameInterests() ) )
    else:
        log.error( "ERROR - SiderealEstimations - Input filepath provided has incorrect or no data [{}]".format( sFilepath ) )

if __name__ == "__main__":
    # timestamp to mark the filename
    timeNow = time.gmtime()
    sTimestamp = time.strftime( "%Y.%m.%d_%H%M%S", timeNow )

    # setup log dir
    sLogDir = os.path.join( Common.sLogsDirectory, "SiderealEstimations" )
    sLogFileName = "SiderealEstimations-Debug-" + sTimestamp + ".txt"
    sLogErrorName = "SiderealEstimations-Error-" + sTimestamp + ".txt"

    # setup logging for this runthrough
    CommonLogging.loggingSetup( sLogDir=sLogDir, sLogName=sLogFileName, sErrorDir=sLogDir, sErrorName=sLogErrorName )

    sys.exit( basicDataDump() )
