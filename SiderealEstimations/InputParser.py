'''
Created on Oct 17, 2018

@author: clayton.reid
'''

import os
import csv

from Common import Common

import logging
from xdrlib import ConversionError
log = logging.getLogger( __name__ )

lFactions = [["Caylion", 15, 7],
             ["Eni Et", 7.5, 3.5],
             ["Faderan", 12, 5],
             ["Im'Dril", 18.5, 3],
             ["Kjasjavikalimm", 15.5, 7],
             ["Kt'zr'kt'rtl", 15.5, 5],
             ["Unity", 11.5, 4.5],
             ["Yengii", 12, 5.5],
             ["Zeth", 10.5, 5]]

sFactionUnknown = "UNKNOWN"

class Faction():

    def __init__( self, sFactionName, dStartingValue, dProductionValue ):
        '''
        Constructor
        '''
        # Member Variables
        self.m_sFactionName = sFactionName
        self.m_dStartingValue = float( dStartingValue )
        self.m_dProductionValue = float( dProductionValue )
        self.m_bIsValid = True

        # Validate Member Variables
        self.validate()

    @classmethod
    def initFromFactionName( cls, sFactionName ):
        for sFaction in lFactions:
            if sFactionName.lower() == sFaction[0].lower():
                return cls( sFaction[0], sFaction[1], sFaction[2] )
            elif sFactionName[0:2].lower() == sFaction[0][0:2].lower():
                log.debug( "DEBUG - Faction.matchFactionName - Assumption made on faction name [{}] -> [{}]".format( sFactionName, sFaction ) )
                return cls( sFaction[0], float( sFaction[1] ), int( sFaction[2] ) )

        log.debug( "FAIL - Faction.matchFactionName - Faction name is UNKNOWN [{}]".format( sFactionName ) )
        return cls( sFactionUnknown, 0, 0 )

    def validate( self ):
        self.m_bIsValid = True
        if self.m_sFactionName == sFactionUnknown:
            log.debug( "FAIL - Faction.validate - Invalid due to UKNONWN faction name [{}]".format( self.m_sFactionName ) )
            self.m_bIsValid = False

        if not isinstance( self.m_dStartingValue, float ):
            log.debug( "FAIL - Faction.validate - Invalid due to starting value not float [{}]".format( self.m_dStartingValue ) )
            self.m_bIsValid = False

        if not isinstance( self.m_dProductionValue, float ):
            log.debug( "FAIL - Faction.validate - Invalid due to production value not float [{}]".format( self.m_dProductionValue ) )
            self.m_bIsValid = False

        return self.m_bIsValid

class FactionGameEndData():

    def __init__( self, sFactionName, dScore, iTimesPlayed ):
        '''
        Constructor
        '''
        # Member Variables
        self.m_Faction = Faction.initFromFactionName( sFactionName )
        self.m_dScore = dScore
        self.m_dCubeScore = Common.floatround( self.m_dScore * 6, 2 )
        self.m_iTimesPlayed = iTimesPlayed
        self.m_bIsValid = True
        self.m_fInterest = 0

        # Validate Member Variables
        if not self.m_Faction.m_bIsValid:
            log.debug( "FAIL - FactionGameEndData - Invalid due to Faction not valid [{}]".format( self.m_Faction ) )
            self.m_bIsValid = False

        if self.m_bIsValid:
            self.m_fInterest = self.calculateInterest()

    def __gt__( self, factionGameEndData ):
        return self.m_Faction.m_sFactionName > factionGameEndData.m_Faction.m_sFactionName

    def calculateInterest( self ):
        fInterest = 1.4
        bConverged = False
        while not bConverged:
            fDummyFinalScore = self.calculateFinalScore( fInterest )
            if Common.floatround( fDummyFinalScore, 2 ) == self.m_dCubeScore:
                bConverged = True

            fInterest = fInterest + 0.3 * ( ( self.m_dCubeScore - fDummyFinalScore ) / self.m_dCubeScore )

        return Common.floatround( fInterest, 4 )

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
                        log.debug( "FAIL - GameEndData - Row length is incorrect [{}]".format( row ) )

                    self.m_lFactionGameEndDatas.append( FactionGameEndData( row[0], float( row[1] ), int( row[2] ) ) )

        except FileNotFoundError or ConversionError as e:
            log.debug( "FAIL - GameEndData - Exception caught pulling data from filepath; ignoring data [{}]".format( self.m_sFilepath ) )
            log.debug( "FAIL - GameEndData - [{}]".format( e ) )
            self.m_lFactionGameEndDatas = []
            self.m_bIsValid = False
        except Exception as e:
            log.error( "ERROR - GameEndData - Unexpected exception captured" )
            raise e

        for factionGameEndData in self.m_lFactionGameEndDatas:
            if not factionGameEndData.m_bIsValid:
                self.m_bIsValid = False

        if self.m_bIsValid:
            self.m_lFactionGameEndDatas.sort()

        if self.m_bIsValid:
            fInterestSum = 0
            for factionGameEndData in self.m_lFactionGameEndDatas:
                fInterestSum += factionGameEndData.m_fInterest
            self.m_fGameInterest = fInterestSum / len( self.m_lFactionGameEndDatas )
            self.m_iPlayerCount = len( self.m_lFactionGameEndDatas )
