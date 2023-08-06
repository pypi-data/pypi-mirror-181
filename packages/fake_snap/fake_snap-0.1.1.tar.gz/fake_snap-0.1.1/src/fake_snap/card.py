#define card object
class Card:
    '''
    This is where the details of a card are stored.
    '''
    def __init__(self, id = 0, name = '', cost = 0, power = 0, effect = ''):
        self.id = id
        self.name = name
        self.cost = cost
        self.power = power
        self.effect = effect
    
    #Getters and Setters
    #def getID(self):
    #    return

    def getName(self):
        return self.name
    
    def setName(self, name):
        self.name = name
    
    def getCost(self):
        return self.cost
    
    def setCost(self, cost):
        self.cost = cost
    
    def getPower(self):
        return self.power
    
    def setPower(self, power):
        self.power = power
    
    def getEffect(self):
        return self.effect
    
    def setEffect(self, effect):
        self.effect = effect

    
    #Member Methods
    
