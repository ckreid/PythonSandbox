'''
Author: Clayton Reid
Created on Oct 17, 2018

Description:
Various helper commands and functions.
'''

import subprocess
import time
import os
import shutil
import sys

import logging
log = logging.getLogger( __name__ )

# version information for all tools
sVersionNumber = "1.0"
sVersionDate = "October 17, 2018"

# setup current directory path
sCurrentDirectory = os.path.dirname( os.path.abspath( __name__ ) )
sLogsDirectory = os.path.join( sCurrentDirectory, "LOGS" )

def initializeFolder( sFilepath, bRemoveExisting=True ):
    ''' Initializes a folder path, cleans it or creates it as needed '''
    log.debug( "DEBUG - Intializing {}".format( sFilepath ) )
    bCreateFile = True
    if os.path.exists( sFilepath ):
        if bRemoveExisting:
            log.debug( "DEBUG - Path exists.. deleting path file first" )
            cleanupFolder( sFilepath )
        else:
            log.debug( "DEBUG - Path exists.. but not deleting path" )
            bCreateFile = False

    if bCreateFile:
        lDirectories = []
        sPath = sFilepath
        while True:
            if sPath == None:
                log.error( "ERROR - Filepath root does not exist {}".format( lDirectories ) )
                raise
            if not os.path.exists( sPath ):
                lDirectories.append( sPath )
                sPath = os.path.dirname( sPath )
            else:
                break

        log.debug( "DEBUG - Creating new path folder" )
        for _ in range( len( lDirectories ) ):
            try:
                directory = lDirectories.pop()
                os.mkdir( directory )
            except IOError:
                log.error( "ERROR - Failed to create new path {}".format( directory ) )
                raise

    return sFilepath

def cleanupFolder( sFilepath ):
    ''' Removes existing file recursively '''
    log.debug( "DEBUG - Cleaning {}".format( sFilepath ) )
    iIterations = 1
    while os.path.exists( sFilepath ):
        try:
            log.debug( "DEBUG - Removing detected filepath" )
            shutil.rmtree( sFilepath )
            return True
        except IOError:
            log.debug( "   Path exists and could not cleanup {}".format( sFilepath ) )
            iIterations += 1
            if iIterations > 5:
                log.error( "ERROR - Unable to delete {}".format( sFilepath ) )
                log.error( "   Max attempts exceeded..." )
                break
            else:
                log.debug( "   Retrying: Attempt {}...".format( iIterations ) )
                time.sleep( 2 )
    return False

def floatround( fFloatin, iDecimalplace ):
    return float( "{0:.{prec}f}".format( fFloatin, prec=iDecimalplace ) )

def copyFile( sSource, sDestination ):
    try:
        if os.path.exists( sSource ):
            shutil.copy( sSource, sDestination )
            return True
    except FileNotFoundError:
        log.error( "ERROR - FileNotFound Error during file copy!" )
    except:
        log.error( "ERROR - UNKNOWN Error during file copy!" )
    return False

def removeFile( sSource ):
    try:
        if os.path.exists( sSource ):
            os.remove( sSource )
            return True
    except FileNotFoundError:
        log.error( "ERROR - FileNotFound with file removal!" )
    except:
        log.error( "ERROR - UNKNOWN Error during file removal!" )
    return False

# TODO: Functions that use this should use it correctly
def RunShellCmd( sCmd, sWorkingDir, sSuccessStr, iNumRetry=1, iRetryDelay=0, bLogOutput=True, iTimeOut=None, bShell=False ):
    ''' Cmd - param must be a string '''
    iI = 0
    sStdErr = ""
    while iI < iNumRetry:
        iI = iI + 1
        try:
            MyProc = subprocess.Popen( sCmd,
                                      cwd=sWorkingDir,
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=bShell )
            [out, err] = MyProc.communicate( timeout=iTimeOut )
            iRetCode = MyProc.returncode
            sStdErr = err.decode( encoding='UTF-8', errors='ignore' )
            sStdOut = out.decode( encoding='UTF-8', errors='ignore' )

            if sSuccessStr in sStdOut:
                if bLogOutput:
                    log.debug( 'RunShellCmd: command successful, attempt ' + str( iI ) + '/' + str( iNumRetry ) + ': "' + sCmd + '"' )
                return True, ""
            else:
                if bLogOutput:
                    log.debug( 'RunShellCmd: command NOT successful, attempt {}/{}'.format( iI, iNumRetry ) )
                    log.debug( '    CMD: "{}"'.format( sCmd ) )
                    log.debug( '    Command returned: {0}'.format( iRetCode ) )
                    log.debug( '    stdout={0}'.format( sStdOut ) )
                    log.debug( '    stderr={0}'.format( sStdErr ) )

                # sStdErr may be empty, so look at sStdOut instead
                if ( sStdErr == '' and sStdOut != '' ):
                    sStdErr = sStdOut

        except subprocess.TimeoutExpired:
            if bLogOutput:
                log.debug( 'RunShellCmd: command TIMEOUT, attempt {}/{}'.format( iI, iNumRetry ) )
                log.debug( '    CMD: "{}"'.format( sCmd ) )
            sStdErr = "Process Timeout"
            MyProc.kill()
            time.sleep( 10 )
        except:
            log.error( "RunShellCmd: UNHANDLED EXCEPTION, attempt {}/{}".format( iI, iNumRetry ) )
            log.error( "   Exception: {}".format( sys.exc_info()[0] ) )
            MyProc.kill()
            time.sleep( 10 )

        if iI < iNumRetry:
            time.sleep( iRetryDelay )

    return False, sStdErr

def str2bool( sInputString ):
    if sInputString == None:
        return False
        
    if not isinstance( sInputString, str ):
        log.error( "ERROR - str2bool function converting non-bool input string [{}]".format( sInputString ) )
        log.error( "   Returning False" )
        return False

    if sInputString.lower() in ["false", "f", "0", "no"]:
        return False

    if sInputString.lower() in ["true", "t", "1", "yes"]:
        return True

