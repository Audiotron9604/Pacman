# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        #initializing variables
        count = 0
        food = newFood.asList()
        foodLocation = []
        ghostLocation = []

        #adding each ghost's distance to list
        for ghost in successorGameState.getGhostPositions():
            ghostLocation.append(abs(ghost[0] - newPos[0]) + abs(ghost[1] - newPos[1]))

        #calculating action's worthiness based on ghost distance
        for ghost in successorGameState.getGhostPositions():
            
            #incredibly low score if this action will make pacman hit a ghost
            if ghost == newPos:
                count -= 1000

            #slightly lowered score if movement places pacman close to a ghost
            elif (abs(ghost[0] - newPos[0]) + abs(ghost[1] - newPos[1])) <= 3.5:
                count -= 10

        #adding each food's distance to a list
        for item in food:
            foodLocation.append(abs(newPos[0] - item[0]) + abs(newPos[1] - item[1]))

        #calculating action's worthiness based on food distance
        for currFood in foodLocation:
            
            #increases count if food is nearby
            if currFood <= 4:
                count += 1
            
            #increases slightly if food is medium distance
            elif  4 < currFood <= 15:
                count += 0.2
            
            #barely increases if the food is far away
            else:
                count += 0.1

        return successorGameState.getScore() + count

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        #def for the maximizer of our minimax
        def maximizer(gameState, depth):
            #places all actions in a list
            actions = gameState.getLegalActions(0)
            
            #checks for trivial solutions
            if len(actions)==0 or gameState.isWin() or gameState.isLose() or depth==self.depth:
                return(self.evaluationFunction(gameState), None)
            
            #starting with -infinity, determines the maximum value that is possible
            value = -(float("inf"))
            action = None
            
            for currAction in actions:
                
                successorValue = minimizer(gameState.generateSuccessor(0, currAction), 1, depth)
                successorValue = successorValue[0]
                
                #stores the current highest value action
                if(successorValue > value):
                    value, action = successorValue, currAction
            
            #returns the highest value action
            return(value, action)

        #def for the minimizer of our minimax
        def minimizer(gameState, agentID, depth):
            actions = gameState.getLegalActions(agentID)
            
            #checking for trivial solution
            if len(actions) == 0:
                return(self.evaluationFunction(gameState), None)
            
            #starting with infinity, determines the minimum value that is possible
            value = float("inf")
            action = None

            for currAction in actions:
                
                #if this is the final layer, calculates minimum value, otherwise it traverses deeper
                if(agentID == gameState.getNumAgents() - 1):
                    successorValue = maximizer(gameState.generateSuccessor(agentID, currAction), depth + 1)
                else:
                    successorValue = minimizer(gameState.generateSuccessor(agentID, currAction), agentID + 1, depth)
                successorValue = successorValue[0]
                
                #stores the current lowest value action
                if(successorValue < value):
                    value, action = successorValue, currAction
            
            return(value, action)
        
        #returning determined value
        maximizer = maximizer(gameState, 0)[1]
        return maximizer  

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        #def for the maxValue of our expectimax (copied from the maximizer in our minimax function)
        def maxValue(gameState, depth):
            #places all actions in a list
            actions = gameState.getLegalActions(0)
            
            #checks for trivial solutions
            if len(actions)==0 or gameState.isWin() or gameState.isLose() or depth==self.depth:
                return(self.evaluationFunction(gameState), None)
            
            #starting with -infinity, determines the maximum value that is possible
            value = -(float("inf"))
            action = None
            
            for currAction in actions:
                
                successorValue = expValue(gameState.generateSuccessor(0, currAction), 1, depth)
                successorValue = successorValue[0]
                
                #stores the current highest value action
                if(successorValue > value):
                    value, action = successorValue, currAction
            
            #returns the highest value action
            return(value, action)

        #def for the expValue of our exectimax (a slightly tweaked copy from the minimizer in our minimax)
        def expValue(gameState, agentID, depth):
            #loads all legal actions into list
            actions = gameState.getLegalActions(agentID)
            
            #checking for trivial solution
            if len(actions) == 0:
                return(self.evaluationFunction(gameState), None)
            
            #starting with 0, determines the average value of the successors
            value = 0
            action = None

            for currAction in actions:
                
                #traverses through the succesors and obtains their successor values
                if(agentID == gameState.getNumAgents() - 1):
                    successorValue = maxValue(gameState.generateSuccessor(agentID, currAction), depth + 1)
                else:
                    successorValue = expValue(gameState.generateSuccessor(agentID, currAction), agentID + 1, depth)
                successorValue = successorValue[0]
                
                #converts the total sum of value to the average
                avg = successorValue / len(actions)

                #adds the average to the value
                value += avg
            
            return(value, action)

        maxValue = maxValue(gameState, 0)[1]
        return maxValue

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: For this evaluation function I improved it by adding the 'capsule' factor and weighing all
      the factors in the final answer as fit.
    """
    "*** YOUR CODE HERE ***"
    
    #loading our variables
    position = currentGameState.getPacmanPosition()
    ghostList = currentGameState.getGhostStates()
    capsules = currentGameState.getCapsules()

    foodList = currentGameState.getFood()
    foodList = foodList.asList()


    #checking for trivial solutions
    if currentGameState.isWin():
        return float("inf")
    if currentGameState.isLose():
        return float("-inf")


    #iterates through ghosts and adds their distance to their respective lists
    ghostDistance = []
    scaredGhostDistance=[]
    for ghost in ghostList:
        if ghost.scaredTimer == 0:
            ghostDistance += [util.manhattanDistance(position, ghost.getPosition())]
        elif ghost.scaredTimer > 0:
            scaredGhostDistance += [util.manhattanDistance(position, ghost.getPosition())]


    #finds the minimum distance from each ghost list
    minScaredGhostDistance = -1
    if len(scaredGhostDistance) > 0:
        minScaredGhostDistance = min(scaredGhostDistance)

    minGhostDistance = -1
    if len(ghostDistance) > 0:
        minGhostDistance = min(ghostDistance)


    #calculates the minimum distance to a food
    foodDistance = []
    for food in foodList:
        foodDistance += [util.manhattanDistance(food, position)]
    minFoodDist = min(foodDistance)


    #calculates our value based on all of the factors, weighing certain factors more than others as necessary
    value = scoreEvaluationFunction(currentGameState)
    value -= 1.5 * minFoodDist + 2 * (1.0/minGhostDistance) + 2 * minScaredGhostDistance + 20 * len(capsules) + 4 * len(foodList)
    return value

# Abbreviation
better = betterEvaluationFunction

