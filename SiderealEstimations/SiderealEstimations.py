'''
Created on Oct 17, 2018

@author: clayton.reid
'''

import os
import sys
import time

from .Common import Common, CommonLogging

import logging
log = logging.getLogger(__name__)

def main():
    pass

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

    # TODO: Execute properly
    sys.exit( main() )
