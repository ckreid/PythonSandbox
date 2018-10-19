'''
Created on Oct 17, 2018

@author: clayton.reid
'''

import os
import csv

import logging
log = logging.getLogger(__name__)

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

    def __init__(self, sFactionName, dStartingValue, dProductionValue):
        '''
        Constructor
        '''
        self.m_sFactionName = self.matchFactionName(sFactionName)
        self.m_dStartingValue = dStartingValue
        self.m_dProductionValue = dProductionValue
        self.validate()
        
    def matchFactionName(self, sFactionName):
        for sFaction in lFactions:
            if sFactionName in sFaction:
                return sFaction
            elif sFactionName in sFaction[0:1]:
                log.debug("DEBUG - Faction.matchFactionName - Assumption made on faction name [{}] -> [{}]".format(sFactionName, sFaction))
                return sFaction
            
        return sFactionUnknown
    
    def validate(self):
        self.isValid = True
        if self.m_sFactionName == sFactionUnknown:
            log.debug("DEBUG - Faction.validate - Invalid due to UKNONWN faction name [{}]".format(self.m_sFactionName))
            self.isValid = False
            
        if isinstance(self.m_dStartingValue, float):
            log.debug("DEBUG - Faction.validate - Invalid due to starting value not float [{}]".format(self.m_dStartingValue))
            self.isValid = False
            
        if isinstance(self.m_dProductionValue, float):
            log.debug("DEBUG - Faction.validate - Invalid due to production value not float [{}]".format(self.m_dProductionValue))
            self.isValid = False
            
        return self.isValid
            

class FactionGameEndData():

    def __init__(self, faction, dScore, iTimesPlayed):
        '''
        Constructor
        '''
        self.faction = faction
        self.dScore = dScore
        self.iTimesPlayed = iTimesPlayed
        self.isValid = True
        if not self.faction.isValid:
            log.debug("DEBUG - FactionGameEndData - Invalid due to Faction not valid [{}]".format(self.faction))
            self.isValid = False


class GameEndData():

    def __init__(self, sFilepath):
        '''
        Constructor
        '''
        if not os.path.exists(sFilepath):
            self.isValid = False
        
        self.sFilepath = sFilepath
        self.populateData()
                
    def populateData(self):
        try:
            self.lFactionGameEndDatas = []
            with open(self.sFilepath) as dataFile:
                dataReader = csv.reader(dataFile)
                for i, row in enumerate(dataReader):
                    if i == 0:
                        continue
                    if len(row) != 3:
                        self.isValid = False
                    self.lFactionGameEndDatas.append(FactionGameEndData(row[0], row[1], row[2]))
                    
        except Exception as e:
            log.error("ERROR - GameEndData - Exception caught pulling data from filepath [{}]".format(self.sFilepath))
            raise e
        
