'''
Created on Oct 17, 2018

@author: clayton.reid
'''

import os
import csv

from .Common import Common

import logging
log = logging.getLogger( __name__ )

lFactions = ["Kt'zr'kt'rtl",
             "Caylion",
             "Kjasjavikalimm",
             "Faderan",
             "Unity",
             "Eni Et",
             "Zeth",
             "Yengii",
             "Im'Dril"]

sFactionUnknown = "UNKNOWN"

class Faction():

    def __init__( self, sFactionName, dStartingValue, dProductionValue ):
        '''
        Constructor
        '''
        self.m_sFactionName = self.matchFactionName( sFactionName )
        self.m_dStartingValue = float( dStartingValue )
        self.m_dProductionValue = float( dProductionValue )
        self.m_bIsValid = True
        self.validate()

    def matchFactionName( self, sFactionName ):
        for sFaction in lFactions:
            if sFactionName in sFaction:
                return sFaction
            elif sFactionName in sFaction[0:1]:
                log.debug( "FAIL - Faction.matchFactionName - Assumption made on faction name [{}] -> [{}]".format( sFactionName, sFaction ) )
                return sFaction

        log.debug( "FAIL - Faction.matchFactionName - No name matches input faction name; setting to UNKNOWN [{}]".format( sFaction ) )
        return sFactionUnknown

    def validate( self ):
        self.m_bIsValid = True
        if self.m_sFactionName == sFactionUnknown:
            log.debug( "FAIL - Faction.validate - Invalid due to UKNONWN faction name [{}]".format( self.m_sFactionName ) )
            self.m_bIsValid = False

        if isinstance( self.m_dStartingValue, float ):
            log.debug( "FAIL - Faction.validate - Invalid due to starting value not float [{}]".format( self.m_dStartingValue ) )
            self.m_bIsValid = False

        if isinstance( self.m_dProductionValue, float ):
            log.debug( "FAIL - Faction.validate - Invalid due to production value not float [{}]".format( self.m_dProductionValue ) )
            self.m_bIsValid = False

        return self.m_bIsValid

class FactionGameEndData():

    def __init__( self, faction, dScore, iTimesPlayed ):
        '''
        Constructor
        '''
        # Member Variables
        self.m_Faction = faction
        self.m_dScore = dScore
        self.m_dCubeScore = self.m_dCubeScore * 6
        self.m_iTimesPlayed = iTimesPlayed
        self.m_bIsValid = True
        self.m_fInterest = self.calculateInterest()

        # Validate Member Variables
        self.m_Faction.validate()
        if not self.m_Faction.bIsValid:
            log.debug( "FAIL - FactionGameEndData - Invalid due to Faction not valid [{}]".format( self.faction ) )
            self.m_bIsValid = False

    def calculateInterest( self ):
        fInterest = 1.4
        bConverged = False
        # TODO: DEBUG TEST TO OPTIMIZE WEIGHT
        iSteps = 0
        while not bConverged:
            fDummyFinalScore = self.calculateFinalScore( fInterest )
            if Common.floatround( fDummyFinalScore, 2 ) == self.m_dCubeScore:
                bConverged = True

            fInterest = fInterest + 2 * ( self.m_dCubeScore - fDummyFinalScore / self.m_dCubeScore )
            iSteps += 1

        log.info( "Steps taken: {}".format( iSteps ) )
        return fInterest

    def calculateFinalScore( self, fInterest ):
        fCubeValue = self.m_Faction.m_dStartingValue * ( fInterest ** 6 )
        fProductionValue = self.m_Faction.m_dProductionValue * ( ( 1 - ( fInterest ** 6 ) ) / ( 1 - fInterest ) )
        return fCubeValue + fProductionValue

class GameEndData():

    def __init__( self, sFilepath ):
        '''
        Constructor
        '''
        # Verification
        if not os.path.exists( sFilepath ):
            self.bIsValid = False

        # Member Variables
        self.m_sFilepath = sFilepath
        self.m_lFactionGameEndDatas = []
        self.m_fGameInterest = 0
        self.m_iPlayerCount = 0
        self.m_bIsValid = True
        
        # Populate/Validate Member Variables
        try:
            self.m_lFactionGameEndDatas = []
            with open( self.m_sFilepath ) as dataFile:
                dataReader = csv.reader( dataFile )
                for i, row in enumerate( dataReader ):
                    if i == 0:
                        continue

                    if len( row ) != 3:
                        self.m_bIsValid = False

                    self.m_lFactionGameEndDatas.append( FactionGameEndData( row[0], float( row[1] ), float( row[2] ) ) )

        except Exception as e:
            log.debug( "FAIL - GameEndData - Exception caught pulling data from filepath; ignoring data [{}]".format( self.sFilepath ) )
            log.debug( "FAIL - GameEndData - " )
            log.debug( "FAIL - GameEndData - [{}]".format( e ) )
            self.m_lFactionGameEndDatas = []
            self.m_bIsValid = False

        fInterestSum = 0
        for factionGameEndData in self.m_lFactionGameEndDatas:
            fInterestSum += factionGameEndData.m_fInterest
        self.m_fGameInterest = fInterestSum / len( self.m_lFactionGameEndDatas )
        self.m_iPlayerCount = len( self.m_lFactionGameEndDatas )
