'''
Created by Joey and Noah Wheeler 11/22/22

This is a parody.  This is not intended to commercially compete with any real or fictional IP.
Don't Sue.  We have no money.

Goal 1. Create Shuffler to track cards played, engine will be done on paper.
Goal 2. Add game and mechanics... maybe... if we have time eventually.

'''


import game
import deck
import location

#debug Tools
DEBUG = False #Switch this to True for more verbose debugging.


#define player object
class Player:
    '''
    This is the player object.  This is where information only relevant to the player is stored.
    '''
    def __init__(self, position = 0, energy = 0):
        self.energy = energy
        self.position = position
    
    #Getters and Setters
    def getEnergy(self):
        return self.energy
    
    def getPosition(self):
        return self.position
    
    #Member Methods
    def incrementEnergy(self):
        self.energy += 1

#define board object
class Board:
    '''
    This is the board object.  This is where the locations, and cards played at those locations are stored.
    '''
    def __init__(self,locations = ['null_loc','null_loc','null_loc'],lanes = [[['','','',''],['','','',''],['','','','']],[['','','',''],['','','',''],['','','','','']]]):
        self.locations = locations
        self.lanes = lanes


#define hand object
class Hand(object):
    '''
    This is where a players hand information is stored. Each players hand holds 7 cards max.
    '''
    def __init__(self, cards = []):
        self.cards = cards
    
    def getCards(self):
        return self.cards
    
    def setCards(self,cards):
        self.cards = cards
    
    def addCard(self,card):
        self.cards.append(card)
    
    #member methods

    def cardCount(self):
        return len(self.getCards())


#define card object
class Card:
    '''
    This is where the details of a card are stored.
    '''
    def __init__(self, cost = 0, power = 0, effect = ''):
        self.cost = cost
        self.power = power
        self.effect = effect


#Function Definitions for this file

def draw(deck, hand):
    #Only draw if hand not full
    if hand.cardCount() <= 6:
        hand.addCard(deck.getCards()[0])
        deck.popTop()
    else:
        print("Hand Full.  Cannot draw more cards")

#-----Instantiate Game Object
game = game.Game()

#-----Instantiate Player Object
p1 = Player(1)
p2 = Player(2)

#-----Instantiate Deck Objects
p1Deck = deck.Deck()
p2Deck = deck.Deck()

#-----Instantiate Location Objects
leftLocation = location.Location()
midLocation = location.Location()
rightLocation = location.Location()

#---Roll Locations
leftLocation.rollLocation(debugging=DEBUG)

midLocation.rollLocation(debugging=DEBUG)
while (midLocation.getID() == leftLocation.getID()): #Handle Duplicate Locations
    midLocation.rollLocation(debugging=DEBUG)

rightLocation.rollLocation(debugging=DEBUG)
while (rightLocation.getID() == leftLocation.getID() or rightLocation.getID() == midLocation.getID()):  #Handle Duplicate Locations
    rightLocation.rollLocation(debugging=DEBUG)


#-----Parse JSON file into deck object for both players
p1Deck.loadDeck(1,debugging=DEBUG)
p2Deck.loadDeck(2,debugging=DEBUG)

#--instantiate hand objects
#No idea why I have to initialize this with something in the contructor.  
#If I don't, both are treated as the same object even though the debugger says they are seperate instances.
p1Hand = Hand([])
p2Hand = Hand([])


#call deck shuffle method for each deck
p1Deck.shuffle()
if DEBUG == True:
    print(f'Shuffled P1 Deck: {p1Deck.getCards()}')

p2Deck.shuffle()
if DEBUG == True:
    print(f'Shuffled P2 Deck: {p2Deck.getCards()}')

#-----Game Loop
#Print Locations
print(f'\nLeft Location: {leftLocation.getName()}')
print(f'Mid Location: {midLocation.getName()}')
print(f'Right Location: {rightLocation.getName()}')

#Set Turn Counter
game.nextTurn()
print(f'\nCurrent Turn: {game.getTurn()}')

#Calculate Player Priority
game.determinePriority()
print(f'Priority: {game.getPriority()}')

#Set Energy
p1.incrementEnergy()
p2.incrementEnergy()
print(f'P1 Energy: {p1.getEnergy()}')
print(f'P2 Energy: {p2.getEnergy()}')

#Reveal Location and Trigger Location Effect
if(game.getTurn() == 1):
    leftLocation.activate()
elif(game.getTurn() == 2):
    midLocation.activate()
elif(game.getTurn() == 3):
    rightLocation.activate()



#call draw method (x4) for turn one
print(f'Hand Player One: {p1Hand.getCards()}')
print(f'Hand Player Two: {p2Hand.getCards()}')
print('Drawing...')
for d in range(4):
    draw(p1Deck,p1Hand)
    draw(p2Deck,p2Hand)
    
print(f'Hand Player One: {p1Hand.getCards()}')
print(f'Hand Player Two: {p2Hand.getCards()}')
print(f'Deck Player One: {p1Deck.getCards()}')
print(f'Deck Player Two: {p2Deck.getCards()}')


#Check What Cards are playable
#TODO For this, I will need the card database entries for the cards in the JSON File
#---Main Turn Loop