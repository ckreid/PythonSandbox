'''
Author: Clayton Reid
Created on Oct 17, 2018

Description:
Contains helper functions and configurations for initializing Python logging.
The user has to run loggingSetup(...), and fill in what information he needs;
if debug logs or error logs file path is empty, it will not create them.

Use:
At the beginning of the main file, the below needs to be added:
    import logging
    import CommonLogging
    log = logging.getLogger(__name__)

In addition, in the (if __name__ == "__main__":) block, call loggingSetup,
following the steps found in the functions description.

After those steps, the system will be setup, and throughout your code you will
simply call log.* (debug, info, error, etc), where it will store information
into the various log streams based on their configurations.

To use logging in any other modules used or called by the main module,
simply add the below, then use the log.* as needed.
    import logging
    log = logging.getLogger(__name__)
'''

import logging
import os
import sys

global logFilePath
global errorFilePath
rootLog = logging.getLogger()

FORMAT_CONSOLE = '%(asctime)s: %(message)s'
FORMAT_TIME_CONSOLE = '%H:%M:%S'
FORMAT_LOG = '%(asctime)s %(levelname)s: %(message)s'
FORMAT_ERROR = '%(asctime)s %(levelname)s %(pathname)s %(lineno)d: %(message)s'

###############################################################################
# Takes as input a stream for which the logging will stream out to. Typically,
# this stream will be the default sys.stdout.
#
# [stream]        - the stream in which output data is sent
#
def configureInfoStream( stream ):
    '''
    Takes as input a stream for which the logging will stream out to. Typically,
    this stream will be the default sys.stdout.
    '''
    ch = logging.StreamHandler( stream )
    ch.setLevel( logging.INFO )
    streamFormatter = logging.Formatter( FORMAT_CONSOLE, FORMAT_TIME_CONSOLE )
    ch.setFormatter( streamFormatter )
    rootLog.addHandler( ch )

###############################################################################
# Takes as input a directory and a filename of which a log file will be
# generated and populated. This will automatically generate a directory if it
# is missing.
#
# [logDir]        - the file path to the directory the file will be stored
# [logName]       - the name of the log file to be saved
#
def configureLogFile( sLogDir, sLogName ):
    global g_sLogFilePath
    if sLogDir != '':
        if not os.path.exists( sLogDir ):
            os.makedirs( sLogDir )

    g_sLogFilePath = os.path.join( sLogDir, sLogName )
    fh = logging.FileHandler( g_sLogFilePath, 'w' )
    fh.setLevel( logging.DEBUG )
    logFormatter = logging.Formatter( FORMAT_LOG )
    fh.setFormatter( logFormatter )
    rootLog.addHandler( fh )

###############################################################################
# Takes as input a directory and a filename of which a error log file will be
# generated and populated. This will automatically generate a directory if it
# is missing.
#
# [errorDir]      - the file path to the directory the file will be stored
# [errorName]     - the name of the log file to be saved
#
def configureErrorFile( sErrorDir, sErrorName ):
    global g_sErrorFilePath
    if sErrorDir != '':
        if not os.path.exists( sErrorDir ):
            os.makedirs( sErrorDir )

    g_sErrorFilePath = os.path.join( sErrorDir, sErrorName )
    ef = logging.FileHandler( g_sErrorFilePath, 'w' )
    ef.setLevel( logging.ERROR )
    errorFormatter = logging.Formatter( FORMAT_ERROR )
    ef.setFormatter( errorFormatter )
    rootLog.addHandler( ef )

###############################################################################
# Returns the file path of the generated log file
def getLogFilePath():
    return g_sLogFilePath

# Returns the file path of the generated error file
def getErrorFilePath():
    return g_sErrorFilePath

###############################################################################
# Core setup function of the system, taking various inputs to generate all
# of the various StreamHandlers and FileHandlers. Any information not given,
# will result in that file system not being created and used in the logging.
#
# [sLogDir]                - the path to the directory of the log file
# [sLogName]               - the name of the log file to be saved
# [sErrorDir]              - the path to the directory of the error file
# [sErrorName]             - the name of the error file to be saved
#
# eg. CommonLogging.loggingSetup(C:\\Dejero\\logs\\, debug.txt)
#    - this will generate a sys.stdout debug stream as well as a FileHandler
#    for a file found at C:\\Dejero\\logs\\debug.txt and populate it
#
def loggingSetup( sLogDir='', sLogName='', sErrorDir='', sErrorName='' ):
    rootLog.setLevel( logging.DEBUG )
    configureInfoStream( sys.stdout )
    if sLogName != '':
        configureLogFile( sLogDir, sLogName )

    if sErrorName != '':
        configureErrorFile( sErrorDir, sErrorName )
