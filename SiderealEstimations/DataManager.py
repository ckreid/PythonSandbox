'''
Created on Oct 19, 2018

@author: clayton.reid
'''

import os

import InputParser

import logging
log = logging.getLogger( __name__ )

class GameEndDataManager():
    '''
    classdocs
    '''

    def __init__( self, sDataInputFolder ):
        '''
        Constructor
        '''
        if not os.path.isdir( sDataInputFolder ):
            log.error( "ERROR - GameEndDataManager - Input folder either does not exist or is not a directory [{}]".format( sDataInputFolder ) )
            raise

        self.m_gameEndDatas = []
        for sDataFile in os.listdir( sDataInputFolder ):
            gameEndData = InputParser.GameEndData( os.path.join( sDataInputFolder, sDataFile ) )
            if gameEndData.m_IsValid:
                self.m_gameEndDatas.append( gameEndData )

    def averageInterest( self ):
        fInterestSum = 0
        iValidEntries = 0
        for gameEndData in self.m_gameEndDatas:
            if not gameEndData.m_bIsValid:
                continue

            iValidEntries = gameEndData.numberOfPlayers()

        return fInterestSum / iValidEntries
