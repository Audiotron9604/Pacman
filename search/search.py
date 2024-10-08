# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    
    dfsStack = util.Stack()                                            #defining variables
    startNode = (problem.getStartState(), [])
    visitedNodes = []

    dfsStack.push(startNode)
    
    while not dfsStack.isEmpty():
        currentNode = dfsStack.pop()
        nodeLocation = currentNode[0]                                 #traversing to next node and obtaining its location and path
        currentPath = currentNode[1]
        
        if visitedNodes.__contains__(nodeLocation):                 #skips node if it's already visited
            continue
        else:                        
            visitedNodes.append(nodeLocation)                       #marks node as visited
            
            if problem.isGoalState(nodeLocation):                   #returns path if node is the goal
                return currentPath                            
            
            successors = problem.getSuccessors(nodeLocation)
            for currentSuccessor in list(successors):               #adds every successor that hasn't already been visited to the stack
                if not visitedNodes.__contains__(currentSuccessor):
                    dfsStack.push((currentSuccessor[0], currentPath + [currentSuccessor[1]]))
    return []


    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    bfsQueue = util.Queue()                                            #defining variables
    startNode = (problem.getStartState(), [])
    visitedNodes = []

    bfsQueue.push(startNode)
    
    while not bfsQueue.isEmpty():
        currentNode = bfsQueue.pop()
        nodeLocation = currentNode[0]                                 #traversing to next node and obtaining its location and path
        currentPath = currentNode[1]
        
        if visitedNodes.__contains__(nodeLocation):                 #skips node if it's already visited
            continue
        else:                        
            visitedNodes.append(nodeLocation)                       #marks node as visited
            
            if problem.isGoalState(nodeLocation):                   #returns path if node is the goal
                return currentPath                            
            
            successors = problem.getSuccessors(nodeLocation)
            for currentSuccessor in list(successors):               #adds every successor that hasn't already been visited to the queue
                if not visitedNodes.__contains__(currentSuccessor):
                    bfsQueue.push((currentSuccessor[0], currentPath + [currentSuccessor[1]]))
    return []
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    
    pqueue = util.PriorityQueue()
    currentState = problem.getStartState()
    node = {}
    node["predeccessor"] = None                                     #defining variables
    node["action"] = None                                           #utilizing a dictionary to deal with each states multiple values
    node["cost"] = 0
    node["state"] = currentState
    visitedNodes = []

    pqueue.push(node, node["cost"])

    while not pqueue.isEmpty():
        node = pqueue.pop()
        currentCost = node["cost"]                                  #loads next node
        currentState = node["state"]

        if(visitedNodes.__contains__(currentState)):
            continue                                                #skips if already visited, if not, marks as visited
        visitedNodes.append(currentState)

        if problem.isGoalState(currentState):                       #determines if current state is the goal state
            break

        for currentSuccessor in problem.getSuccessors(currentState):
            if not visitedNodes.__contains__(currentSuccessor[0]):
                newNode = {}
                newNode["state"] = currentSuccessor[0]              #adding successors that haven't already been visited to the priority queue
                newNode["action"] = currentSuccessor[1]
                newNode["predeccessor"] = node
                newNode["cost"] = currentSuccessor[2] + currentCost
                pqueue.push(newNode, newNode["cost"])

    solution = []
    while node["action"] != None:
        solution.insert(0, node["action"])                           #compiling solution into a list
        node = node["predeccessor"]
    return solution

    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    
    pqueue = util.PriorityQueue()
    currentState = problem.getStartState()
    node = {}
    node["predeccessor"] = None                                     #defining variables
    node["action"] = None                                           #utilizing a dictionary to deal with each states multiple values
    node["cost"] = 0
    node["heuristic"] = heuristic(currentState, problem)
    node["state"] = currentState
    visitedNodes = []

    pqueue.push(node, node["cost"] + node["heuristic"])

    while not pqueue.isEmpty():
        node = pqueue.pop()
        currentCost = node["cost"]                                  #loads next node
        currentState = node["state"]
        currentHeuristic = node["heuristic"]

        if(visitedNodes.__contains__(currentState)):
            continue                                                #skips if already visited, if not, marks as visited
        visitedNodes.append(currentState)

        if problem.isGoalState(currentState):                       #determines if current state is the goal state
            break

        for currentSuccessor in problem.getSuccessors(currentState):
            if not visitedNodes.__contains__(currentSuccessor[0]):
                newNode = {}
                newNode["state"] = currentSuccessor[0]              #adding successors that haven't already been visited to the priority queue
                newNode["action"] = currentSuccessor[1]
                newNode["predeccessor"] = node
                newNode["cost"] = currentSuccessor[2] + currentCost
                newNode["heuristic"] = heuristic(newNode["state"], problem)
                pqueue.push(newNode, newNode["cost"] + newNode["heuristic"])

    solution = []
    while node["action"] != None:
        solution.insert(0, node["action"])                           #compiling solution into a list
        node = node["predeccessor"]
    return solution

    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
