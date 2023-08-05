'''
This is the module where everything related to the game state is located.  Score will belong here
because it is relevant to determining the winner.  It affects each Player, but is not an attribute of that Player.
'''

import random

#define Game object
class Game:
    '''
    This is the game object.  This is where the turn count, score, play first priority, and game outcome are stored.
    '''
    #Constructors
    def __init__(self,turn = 0, score = [[0,0,0],[0,0,0]], priority = 0, decision = 0):
        self.turn = turn
        self.score = score
        self.priority = priority
        self.decision = decision

    #Getters and Setters
    def getTurn(self):
        return self.turn
    
    def nextTurn(self):
        self.turn += 1

    def getPriority(self):
        return self.priority
    
    def setPriority(self,newPriority):
        self.priority = newPriority
    
    def getScore(self):
        return self.score
    
    def getP1LeftScore(self):
        return self.score[0][0]
    
    def getP1MidScore(self):
        return self.score[0][1]
    
    def getP1RightScore(self):
        return self.score[0][2]
    
    def getP2LeftScore(self):
        return self.score[1][0]
    
    def getP2MidScore(self):
        return self.score[1][1]
    
    def getP2RightScore(self):
        return self.score[1][2]
    
    def setScore(self,newScore):
        self.score = newScore
    
    #Member Methods
    
    def determinePriority(self):
        priorityArr = [0,0]

        #Evaluate Left Lane
        if self.getP1LeftScore() > self.getP2LeftScore():
            priorityArr[0] += 1     #Player One winning left lane
        elif self.getP1LeftScore() < self.getP2LeftScore():
            priorityArr[1] += 1     #Player Two winning left lane
        
        #Evaluate Mid Lane
        if self.getP1MidScore() > self.getP2MidScore():
            priorityArr[0] += 1     #Player One winning mid lane
        elif self.getP1MidScore() < self.getP2MidScore():
            priorityArr[1] += 1     #Player Two winning mid lane

        #Evaluate Right Lane
        if self.getP1RightScore() > self.getP2RightScore():
            priorityArr[0] += 1     #Player One winning right lane
        elif self.getP1RightScore() < self.getP2RightScore():
            priorityArr[1] += 1     #Player Two winning right lane

        #Calc Winning
        if priorityArr[0] > priorityArr [1]: #Player One Winning
            self.setPriority(1)     #Player One goes first
        elif priorityArr[0] < priorityArr [1]: #Player Two Winning
            self.setPriority(2)     #Player Two goes first
        else:
            #Board is a Tie, 50/50
            if random.randint(0,1) == 0:
                self.setPriority(1) #Player One goes first
            else:
                self.setPriority(2) #Player Two goes first