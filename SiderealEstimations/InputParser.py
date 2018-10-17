'''
Created on Oct 17, 2018

@author: clayton.reid
'''

lFactions = ["Kt'zr'kt'rtl",
             "Caylion",
             "Kjasjavikalimm",
             "Faderan",
             "Unity",
             "Eni Et",
             "Zeth",
             "Yengii",
             "Im'Dril"]

class Faction():

    def __init__( self, sFactionName, dStartingValue, dProductionValue ):
        '''
        Constructor
        '''
        self.m_sFactionName = self.matchFactionName( sFactionName )
        self.m_dStartingValue = dStartingValue
        self.m_dProductionValue = dProductionValue

class FactionGameEndData():
    '''
    classdocs
    '''

    def __init__( self, faction, ):
        '''
        Constructor
        '''

class GameEndData():
    '''
    classdocs
    '''

    def __init__( self, sFilepath ):
        '''
        Constructor
        '''
