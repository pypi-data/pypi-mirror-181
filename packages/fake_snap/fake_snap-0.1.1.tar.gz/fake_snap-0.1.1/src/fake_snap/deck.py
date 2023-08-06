'''
This is the Deck Module.  Everything related to the players decks is stored here.
'''

import random
import json

#define deck object
class Deck:
    '''
    This is where the deck information is stored.  Each players deck holds 12 cards.
    '''
    #Constructors
    def __init__(self, cards = ['','','','','','','','','','','','']):
        self.cards = cards
    
    #Getters and Setters
    def getCards(self):
        return self.cards

    def setCards(self,card_list):
        self.cards = card_list
    
    #Member Methods
    
    def popTop(self):
        self.cards.pop(0)

    def shuffle(self):
        random.shuffle(self.cards)
    
    def loadDeck(self, playerPosition, debugging = False):
        '''
        We are going to be using files with text in JSON format that will represent the deck of each player.

        Example of JSON:

        {
            "cards": [
                "Wolverine",
                "Lizard",
                "Scorpion",
                "Rhino",
                "Vulture",
                "Wasp",
                ...
            ]
        }
        '''
        #-----Parse JSON file into deck object
        json_file = open(f'src/json/p{playerPosition}_deck.json')
        json_arr = json.load(json_file)

        if debugging == True:
            print(f'Player {playerPosition} Cards:\n {json_arr["cards"]}')
            for card in json_arr["cards"]:
                print(card)

        #Store parsed json in object
        self.setCards(json_arr["cards"])

        if debugging == True:
            print(f'The p{playerPosition}Deck Object contains {self.getCards()}')

        #Close deck json file
        json_file.close()