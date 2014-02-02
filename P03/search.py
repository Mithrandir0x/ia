# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
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
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]


def recursive_depthFirstSearch(problem):
    """
    Recursive version of the DFS. Inefficient, compared to the default one.
    """
    marked = {}
    edgeTo = {}
    goal = []
    
    def performDFS(node):
        marked[str(node)] = True
        if problem.isGoalState(node):
            goal.append(node)
        for successor in problem.getSuccessors(node):
            if not str(successor[0]) in marked:
                edgeTo[str(successor[0])] = [node, successor[1]]
                performDFS(successor[0])

    def pathTo(node):
        path = util.Queue()
        n = node
        s = problem.getStartState()
        while n != s:
            path.push(edgeTo[str(n)][1])
            n = edgeTo[str(n)][0]
        return path
    
    performDFS(problem.getStartState())
    return pathTo(goal[0]).list

def genericSolver(problem, dataStrategy, isPriorityQueue = False):
    """
    As DFS, BFS and UCS perform in the same way, and only differ in the structure
    used to save the candidates to be observed, this method implements all the funcionality
    and allows to change the data strategy.

    For easier implementation, it is necessary to state if a Priority Queue is passed as
    data strategy.
    """
    marked = []
    edgeTo = {}
    frontier = dataStrategy

    def expand(state):
        """
        Expands from the state passed by and returns the goal state, thus solving the problem.
        """
        cost = 1
        frontier.push(state)
        while not frontier.isEmpty():
            state = frontier.pop()
            marked.append(state)
            for successor in problem.getSuccessors(state):
                newState, action = successor[0], successor[1]
                if ( not newState in marked ) and ( not newState in frontier.list ):
                    edgeTo[newState] = [state, action]
                    frontier.push(newState)
            if problem.isGoalState(state):
                return state
        raise Exception('No solution available')

    def pathTo(state):
        """
        Returns an array of Directions values indicating the path to the state.
        """
        path = util.Queue()
        n = state
        s = problem.getStartState()
        while n != s:
            # print n, edgeTo[n][1]
            path.push(edgeTo[n][1])
            n = edgeTo[n][0]
        return path

    goal = expand(problem.getStartState())
    # path = util.Queue()
    # print edgeTo, len(edgeTo)
    # print
    # print frontier
    
    path = pathTo(goal)

    # print problem.getStartState()
    # print goal
    # print path
    # print pathTo(goal)

    return path.list


def depthFirstSearch(problem):
    """
    This algorithm performs an interative Depth First Search to find the yummy food.
    """
    return genericSolver(problem, util.Stack())


def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    return genericSolver(problem, util.Queue())

def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    return genericSolver(problem, util.PriorityQueue(), True)

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    marked = []
    edgeTo = {}
    frontier = util.PriorityQueue()
    gCost = {}
    fCost = {}

    def expand(state):
        gCost[state] = 0
        fCost[state] = heuristic(state, problem)
        frontier.push(state, fCost[state])

        while (not frontier.isEmpty()):
            state = frontier.pop()
            # marked.append(state)
            for successor in problem.getSuccessors(state):
                newState, action, cost = successor[0], successor[1], successor[2]
                # print newState, action, cost
                if (newState not in marked and newState not in frontier.heap):
                # if newState not in marked:
                    gCost[newState] = gCost[state] + cost
                    fCost[newState] = gCost[newState] + heuristic(newState, problem) 
                    edgeTo[newState] = [state, action]
                    marked.append(newState)
                    frontier.push(newState, fCost[newState]) # fCost[newState]
        
            # print len(frontier.heap)

            if (problem.isGoalState(state)):
                return state

        raise Exception("PETA")

    def pathTo(state):
        """
        Returns an array of Directions values indicating the path to the state.
        """
        path = util.Queue()
        n = state
        s = problem.getStartState()
        while n != s:
            # print n, edgeTo[n][1]
            path.push(edgeTo[n][1])
            n = edgeTo[n][0]
        return path

    goal = expand(problem.getStartState())
    path = pathTo(goal)
    # print path.list
    return path.list


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
