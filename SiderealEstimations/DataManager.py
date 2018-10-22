'''
Created on Oct 19, 2018

@author: clayton.reid
'''

import os

from Common import Common
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
        # Member Variables
        self.m_lGameEndDatas = []
        self.m_bIsValid = True

        # Populate/Verify Member Variables
        if os.path.isdir( sDataInputFolder ):
            for sDataFile in os.listdir( sDataInputFolder ):
                sDataFilepath = os.path.join( sDataInputFolder, sDataFile )
                if os.path.isdir( sDataFilepath ):
                    for sFolderDataFile in os.listdir( sDataFilepath ):
                        gameEndData = InputParser.GameEndData( os.path.join( sDataFilepath, sFolderDataFile ) )
                        if gameEndData.m_bIsValid:
                            self.m_lGameEndDatas.append( gameEndData )
                else:
                    gameEndData = InputParser.GameEndData( sDataFilepath )
                    if gameEndData.m_bIsValid:
                        self.m_lGameEndDatas.append( gameEndData )
        else:
            log.debug( "ERROR - GameEndDataManager - Input folder either does not exist or is not a directory [{}]".format( sDataInputFolder ) )
            self.m_bIsValid = False

        if self.m_bIsValid:
            if not self.m_lGameEndDatas:
                log.debug( "FAIL - GameEndDataManager - No valid data was captured" )
                self.m_bIsValid = False

    def getAverageGameInterest( self ):
        fInterestSum = 0
        iValidEntries = 0
        for gameEndData in self.m_lGameEndDatas:
            iValidEntries += 1
            fInterestSum += gameEndData.m_fGameInterest

        if iValidEntries > 0:
            return Common.floatround( fInterestSum / iValidEntries, 4 )
        else:
            return 0

    def getFactionGameEndDatasWithFaction( self, sFactionName ):
        factionGameEndDatas = []
        for gameEndData in self.m_lGameEndDatas:
            for factionGameEndData in gameEndData.m_lFactionGameEndDatas:
                if factionGameEndData.m_Faction.m_sFactionName == sFactionName:
                    factionGameEndDatas.append( factionGameEndData )

        return factionGameEndDatas

    def getGameEndDatasWithFaction( self, sFactionName ):
        gameEndDatas = []
        for gameEndData in self.m_lGameEndDatas:
            for factionGameEndData in gameEndData.m_lFactionGameEndDatas:
                if factionGameEndData.m_Faction.m_sFactionName == sFactionName:
                    gameEndDatas.append( gameEndData )
                    break

        return gameEndDatas

    def getFactionAverageInterest( self, sFactionName ):
        factionGameEndDatas = self.getFactionGameEndDatasWithFaction( sFactionName )
        if not factionGameEndDatas:
            return 0

        fInterest = 0
        for factionGameEndData in factionGameEndDatas:
            fInterest += factionGameEndData.m_fInterest

        return Common.floatround( fInterest / len( factionGameEndDatas ), 4 )

    def getFactionAverageGameInterest( self, sFactionName ):
        gameEndDatas = self.getGameEndDatasWithFaction( sFactionName )
        if not gameEndDatas:
            return 0

        fInterest = 0
        for gameEndData in gameEndDatas:
            fInterest += gameEndData.m_fGameInterest

        return Common.floatround( fInterest / len( gameEndDatas ), 4 )

    def printAllInterestsPerGame( self ):
        iGameNumber = 1
        sOutputString = ""
        for i, gameEndData in enumerate( self.m_lGameEndDatas ):
            if i > 0:
                sOutputString += "\n"
            sOutputString += "Game {}:".format( iGameNumber )
            for factionGameEndData in gameEndData.m_lFactionGameEndDatas:
                sOutputString += " [{}, {}]".format( factionGameEndData.m_Faction.m_sFactionName, factionGameEndData.m_fInterest )
            iGameNumber += 1

        return sOutputString

    def printAllFactionAverageInterests( self ):
        sOutputString = ""
        for i, defaultFactions in enumerate( InputParser.lFactions ):
            fAverageInterest = self.getFactionAverageInterest( defaultFactions[0] )
            if i > 0:
                sOutputString += "\n"
            sOutputString += "{:14} - {}".format( defaultFactions[0], fAverageInterest )

        return sOutputString

    def printAllFactionAverageGameInterests( self ):
        sOutputString = ""
        for i, defaultFactions in enumerate( InputParser.lFactions ):
            fAverageInterest = self.getFactionAverageGameInterest( defaultFactions[0] )
            if i > 0:
                sOutputString += "\n"
            sOutputString += "{:14} - {}".format( defaultFactions[0], fAverageInterest )

        return sOutputString
