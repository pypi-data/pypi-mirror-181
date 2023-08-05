'''
All the mechanics involving locations are stored here.  See Locations.json for the complete location data.
'''

import json
import random

#define location object
class Location:
    '''
    Everything specifically related to locations is stored here.
    '''
    def __init__(self,id = 0, name = 'empty', effect = '', active = False):
        self.id = id
        self.name = name
        self.effect = effect
        self.active = active
    
    #Getters and Setters
    def getID(self):
        return self.id
    
    def setID(self, newID):
        self.id = newID
    
    def getName(self):
        return self.name

    def setName(self, newName):
        self.name = newName
    
    def getEffect(self):
        return self.effect

    def setEffect(self, newEffect):
        self.effect = newEffect
    
    def getActive(self):
        return self.active
    
    def setActive(self, bool):
        self.active = bool

    #Member Methods
    
    def activate(self):
        self.setActive(True)
        print(self.getName() + " is now active!")
        print("Activating Effect: " + self.getEffect()) #This will call the actual effect by id from a table of functions somewhere in the future.

    def rollLocation(self, debugging = False):
        '''
        Example of JSON:

        {
            "locations": [
                {
                    "id": 1,	
                    "name": "Asgard",
                    "effect": "After turn 4, whoever is winning here draws 2 cards"
                },
                {
                    "id": 2,
                    "name": "Atlantis",
                    "effect": "If you only have one card here, it has +5 Power"
                },
                ...
        '''
        json_file = open(f'src/json/locations.json')
        json_arr = json.load(json_file)

        self.id = random.randint(0,len(json_arr["locations"]) -1)
        #Handle Locations that shouldn't be rolled
        while (self.id == 19 or self.id == 20):
            self.id = random.randint(0,len(json_arr["locations"]) -1)

        self.name = json_arr["locations"][self.id]["name"]
        self.effect = json_arr["locations"][self.id]["effect"]
