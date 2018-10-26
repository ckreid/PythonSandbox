'''
Created on Oct 19, 2018

@author: clayton.reid
'''

import os

from Common import Common
import InputParser

import logging
from InputParser import FactionGameEndData
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
        fTimesPlayed = 0
        for gameEndData in self.m_lGameEndDatas:
            iValidEntries += 1
            fInterestSum += gameEndData.m_fGameInterest
            fTimesPlayed += gameEndData.m_fTimesPlayed

        if iValidEntries > 0:
            return Common.floatround( fInterestSum / iValidEntries, 4 ), iValidEntries, round( fTimesPlayed / iValidEntries, 2 )
        else:
            return 0, 0, 0

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

    def getFactionAverageInterestStats( self, sFactionName ):
        factionGameEndDatas = self.getFactionGameEndDatasWithFaction( sFactionName )
        iNumEntries = len( factionGameEndDatas )
        if not factionGameEndDatas:
            return 0, 0, 0, 0

        fInterest = 0
        iTimesPlayed = 0
        fScore = 0
        for factionGameEndData in factionGameEndDatas:
            fInterest += factionGameEndData.m_fInterest
            iTimesPlayed += factionGameEndData.m_iTimesPlayed
            fScore += factionGameEndData.m_fScore

        return Common.floatround( fInterest / iNumEntries, 4 ), Common.floatround( fScore / iNumEntries, 1 ), iNumEntries, round( iTimesPlayed / iNumEntries, 2 )

    def getFactionAverageGameInterestStats( self, sFactionName ):
        gameEndDatas = self.getGameEndDatasWithFaction( sFactionName )
        iNumEntries = len( gameEndDatas )
        if not gameEndDatas:
            return 0, 0, 0, 0

        fInterest = 0
        fTimesPlayed = 0
        fAverageScore = 0
        fFactionPlusMinus = 0
        for gameEndData in gameEndDatas:
            fInterest += gameEndData.m_fGameInterest
            fTimesPlayed += gameEndData.m_fTimesPlayed
            fAverageScore += gameEndData.m_fAverageScore

            for factionGameEndData in gameEndData.m_lFactionGameEndDatas:
                if factionGameEndData.m_Faction.m_sFactionName == sFactionName:
                    fFactionPlusMinus += factionGameEndData.m_fScore * 6 - gameEndData.m_fAverageScore
                    break

        return Common.floatround( fInterest / iNumEntries, 4 ), Common.floatround( fFactionPlusMinus / ( iNumEntries * 6 ), 1 ), iNumEntries, round( fTimesPlayed / iNumEntries, 2 )

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

    def printAllScoresPerGame( self ):
        iGameNumber = 1
        sOutputString = ""
        for i, gameEndData in enumerate( self.m_lGameEndDatas ):
            if i > 0:
                sOutputString += "\n"
            sOutputString += "Game {}:".format( iGameNumber )
            for factionGameEndData in gameEndData.m_lFactionGameEndDatas:
                sOutputString += " [{}, {}]".format( factionGameEndData.m_Faction.m_sFactionName, Common.floatround( factionGameEndData.m_fScore, 1 ) )
            iGameNumber += 1

        return sOutputString

    def printAllFactionAverageInterests( self ):
        sOutputString = "{:14} {:8} {:5} {:7} {:14}".format( "Faction", "Interest", "Score", "Entries", "AvgTimesPlayed" )
        for defaultFactions in InputParser.lFactions:
            fAverageInterest, fAverageScore, iNumEntries, iAvgTimesPlayed = self.getFactionAverageInterestStats( defaultFactions[0] )
            sOutputString += "\n{:14}   {:<06}  {:4} {:7}           {:<04}".format( defaultFactions[0], fAverageInterest, fAverageScore, iNumEntries, iAvgTimesPlayed )

        return sOutputString

    def printAllFactionAverageGameInterests( self ):
        sOutputString = "{:14} {:8}  {:8} {:8} {:14}".format( "Faction", "Interest", "Score+/-", "Entries", "AvgTimesPlayed" )
        for defaultFactions in InputParser.lFactions:
            fAverageInterest, fAverageScore, iNumEntries, fAvgTimesPlayed = self.getFactionAverageGameInterestStats( defaultFactions[0] )
            sOutputString += "\n{:14}   {:<06}     {:5} {:7}           {:<04}".format( defaultFactions[0], fAverageInterest, fAverageScore, iNumEntries, fAvgTimesPlayed )

        return sOutputString
