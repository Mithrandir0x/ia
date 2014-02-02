
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
    remaining food (oldFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.
    
    Print out these variables to see what you're getting, then combine them
    to create a masterful evaluation function.
    """
    if successorGameState.isWin():  return float("inf")
    if successorGameState.isLose(): return float("-inf")
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    oldFood = currentGameState.getFood()
    newGhostStates = successorGameState.getGhostStates() 
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    
    def manhattan(xy1, xy2):
      return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])

    score = successorGameState.getScore()

    # Minimum distance where the ghosts begin to be important for Pacman.
    warning_ghost_near = 3

    # Only consider the non scared ghosts. Our priority is survive, not win a lot of points, so
    # Pacman will ignore the scared ghosts, who when are eated increase increases a lot the game score.
    manhattans_ghost = [ manhattan(newPos, ghostState.getPosition()) for ghostState in newGhostStates if ghostState.scaredTimer == 0 ]
    
    # If there ara some ghost alive, take the distance between the nearby one and Pacman, and if it's 
    # lower than the warning distance declared before, Pacman will run away. 
    min_manhattans_ghost = warning_ghost_near;
    if ( len(manhattans_ghost) > 0 ): 
      min_manhattans_ghost = min(manhattans_ghost)

    if ( min_manhattans_ghost < warning_ghost_near ):
      return - (float('inf'))

    # In this point, there are some ghost in the map (all of them out of our warning range), but Pacman
    # is not worried at all, so he'll go to eat some balls (maybe there aren't...). How to get the better one? Well, first of all,
    # we need to know the most nearby food, that should be our objetive. 
    manhattans_food = [ ( manhattan(newPos, food) ) for food in oldFood.asList() ]
    min_manhattans_food = min(manhattans_food)
    
    # If there is some ball, the evaluation function will return the inverse of the Manhattan distance
    # between Pacman and that ball, and increasing to that result the actual score. If there's no ball, will 
    # only return the score, being an obviously worse option.
    inv_min_manhattans_food = 0;
    if ( len(manhattans_food) > 0 and min_manhattans_food > 0 ): 
      inv_min_manhattans_food = (1 / min_manhattans_food)

    return inv_min_manhattans_food + score

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
    The Minimax Agent
  """
    
  def getAction(self, gameState):
    evaluate = self.evaluationFunction
    
    maxDepth = self.depth
    maxGhosts = gameState.getNumAgents() - 1

    def maxValue(state, depth):
      """
      The Pacman maximizing utility function. 
      """
      if depth >= maxDepth or state.isWin() or state.isLose():
        # Terminal condition to leave
        utility = evaluate(state)
        # print "%15s: %s" % ( "u(P, %s)" % depth, utility )
        return utility
      
      # The worst thing a Pacman can do is to be idle without doing anything.
      u = float('-inf')
      
      depth += 1
      # We filter the stop action as it is already defined as the possible initial state
      actions = [ action for action in state.getLegalActions() if action != Directions.STOP ]
      # print "%15s: %s" % ("P", actions)
      for action in actions:
        # For each of the action the Pacman can perform, generate a new state
        # with such action executed, and imagine how the ghosts would behave
        # and minimize pacman's utility value
        # print "%15s: %s" % ( "-->MIN",  action )
        utility = minValue(state.generateSuccessor(0, action), depth)
        u = max(u, utility)
      # print "%15s: %s" % ( "MAX(P, %d)" % depth, u )
      return u

    def minValue(state, depth, ghost_id = None):
      """
      The Ghosts minimizing utility function
      """
      if depth >= maxDepth or state.isWin() or state.isLose():
        # Terminal condition to leave
        utility = evaluate(state)
        # print "%15s: %s" % ( "u(P, %s)" % depth, utility )
        return utility
      
      if ghost_id == None:
        ghost_id = 1
      next_ghost_id = ghost_id + 1
      
      # So why initialize the ghost minimizing utility to these
      # values? The best thing a ghost can do to maximize the
      # pacman's utility would be to be frozen, and quiet.
      # Though that won't happen ever...
      u = float('inf')
      
      # For each ghost, iterate over each of its actions
      # to calculate the utility of the new generated state
      # print "%15s: %s" % ( "G%d" % ghost_id, state.getLegalActions(ghost_id) )
      for action in state.getLegalActions(ghost_id):
        # Always find the minimal utility value of the Pacman.
        # We don't want that pesky guy to win over our ghosts.
        if ghost_id == maxGhosts:
          # print "%15s: %s" % ( "-->MAX(%s)" % ghost_id , action )
          utility = maxValue(state.generateSuccessor(ghost_id, action), depth)
          # print "%15s: %s" % ( "<--MAX(%s)" % ghost_id , utility )
        else:
          # print "%15s: %s" % ( "-->MIN(%s)" % ghost_id , action )
          utility = minValue(state.generateSuccessor(ghost_id, action), depth, next_ghost_id)
          # print "%15s: %s" % ( "<--MIN(%s)" % ghost_id , utility )
        # print "%15s: %s" % ( "BEFORE U(G%s, %s)" % ( ghost_id, depth ), u )
        u = min(u, utility)
        # print "%15s: %s" % ( "AFTER U(G%s, %s)" % ( ghost_id, depth ), u )
      # print "%15s: %s" % ( "MIN(G%s, %s)" % ( ghost_id, depth ), u )
      return u

    actions = [ action for action in gameState.getLegalActions() if action != Directions.STOP ]
    actions_utilities = []
    # print "%15s: %s" % ("P", actions)
    for action in actions:
      # print "%15s: %s" % ( "-->MIN",  action )
      actions_utilities.append((minValue(gameState.generateSuccessor(0, action), 1), action))
      # print ""
    
    best_action = max(actions_utilities)

    #print "LEGAL ACTIONS"
    #for a in actions_utilities:
    #  print "\t\t", a
    #print "BEST ONE:", best_action, "\n"
    
    return best_action[1]


class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    The Alpha-Beta Pruning Minimax Agent.
    You're gonna get so pruned...
  """
    
  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    evaluate = self.evaluationFunction
    maxDepth = self.depth
    maxGhosts = gameState.getNumAgents() - 1

    def maxValue(state, alpha, beta, depth):
      if depth >= maxDepth or state.isWin() or state.isLose():
        utility = evaluate(state)
        # print "%15s: %s" % ( "u(P, %s)" % depth, utility )
        return utility
      
      u = float('-inf')
      
      depth += 1
      actions = [ action for action in state.getLegalActions() if action != Directions.STOP ]
      # print "%15s: %s" % ("P", actions)
      for action in actions:
        # print "%15s: %s" % ( "-->MIN",  action )
        utility = minValue(state.generateSuccessor(0, action), alpha, beta, depth)
        u = max(u, utility)
        
        if u >= beta: 
          # print "Downcut beta" 
          return u
        alpha = max(alpha, u)
        # print "Alpha =", alpha

      # print "%15s: %s" % ( "MAX(P, %d)" % depth, u )
      return u

    def minValue(state, alpha, beta, depth, ghost_id = None):
      if depth >= maxDepth or state.isWin() or state.isLose():
        # Terminal condition to leave
        utility = evaluate(state)
        #print "%15s: %s" % ( "u(P, %s)" % depth, utility )
        return utility
      
      if ghost_id == None:
        ghost_id = 1
      next_ghost_id = ghost_id + 1
      
      u = float('inf')
      
      # print "%15s: %s" % ( "G%d" % ghost_id, state.getLegalActions(ghost_id) )
      for action in state.getLegalActions(ghost_id):
        if ghost_id == maxGhosts:
          # print "%15s: %s" % ( "-->MAX(%s)" % ghost_id , action )
          utility = maxValue(state.generateSuccessor(ghost_id, action), alpha, beta, depth)
          # print "%15s: %s" % ( "<--MAX(%s)" % ghost_id , utility )
        else:
          # print "%15s: %s" % ( "-->MIN(%s)" % ghost_id , action )
          utility = minValue(state.generateSuccessor(ghost_id, action), alpha, beta, depth, next_ghost_id)
          # print "%15s: %s" % ( "<--MIN(%s)" % ghost_id , utility )
        # print "%15s: %s" % ( "BEFORE U(G%s, %s)" % ( ghost_id, depth ), u )
        u = min(u, utility)
        
        if u <= alpha:
          # print "Uppercut alpha" 
          return u
        beta = min(beta, u)
        # print "Beta =", beta

        # print "%15s: %s" % ( "AFTER U(G%s, %s)" % ( ghost_id, depth ), u )
      # print "%15s: %s" % ( "MIN(G%s, %s)" % ( ghost_id, depth ), u )
      return u

    actions = [ action for action in gameState.getLegalActions() if action != Directions.STOP ]
    actions_utilities = []
    alpha = float('-inf')
    beta = float('inf')
    # print "%15s: %s" % ("P", actions)
    for action in actions:
      # print "%15s: %s" % ( "-->MIN",  action )
      actions_utilities.append((minValue(gameState.generateSuccessor(0, action), alpha, beta, 1), action))
      # print ""
    
    best_action = max(actions_utilities)

    #print "LEGAL ACTIONS"
    #for a in actions_utilities:
    #  print "\t\t", a
    #print "BEST ONE:", best_action, "\n"

    return best_action[1]

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
  The Expectimax Agent

  This agent is based upon Minimax agent. The idea is that ghosts
  act as probability nodes in the game tree, and their actions are
  considered to have a probability. For now, each action has the
  same probability.
  """
    
  def getAction(self, gameState):
    evaluate = self.evaluationFunction
    
    maxDepth = self.depth
    maxGhosts = gameState.getNumAgents() - 1

    def get_probabilities(state, legal_actions):
      """
      Given a state and a list of legal_actions of a ghost,
      calculate its probabilities.

      Though state is not used in the current implementation,
      having information of the state when calculating the
      probabilities of an action would be useful to know what
      would do a ghost.

      WWGD
      """
      p = {}
      for action in legal_actions:
        p[action] = 1.0 / len(legal_actions)
      return p

    def maxValue(state, depth):
      """
      The Pacman maximizing function. Remains the same as Minimax,
      except for calling expValue, instead of minValue.
      """
      if depth >= maxDepth or state.isWin() or state.isLose():
        # Terminal condition to leave
        utility = evaluate(state)
        # print "%15s: %s" % ( "u(P, %s)" % depth, utility )
        return utility
      
      u = float('-inf')
      
      depth += 1
      actions = [ action for action in state.getLegalActions() if action != Directions.STOP ]
      for action in actions:
        utility = expValue(state.generateSuccessor(0, action), depth)
        u = max(u, utility)
      return u

    def expValue(state, depth, ghost_id = None):
      """
      The Ghost expectation function. Instead of treating the ghost as
      an oponent, it is treated as an external factor, which influences
      the utility function, instead of being an agent which tries to
      minimize the Pacman's utility.
      """
      if depth >= maxDepth or state.isWin() or state.isLose():
        # Terminal condition to leave
        utility = evaluate(state)
        # print "%15s: %s" % ( "u(P, %s)" % depth, utility )
        return utility
      
      if ghost_id == None:
        ghost_id = 1
      next_ghost_id = ghost_id + 1

      actions = state.getLegalActions(ghost_id)
      expectation = 0
      action_probabilities = get_probabilities(state, actions)

      for action in actions:
        if ghost_id == maxGhosts:
          utility = maxValue(state.generateSuccessor(ghost_id, action), depth)
        else:
          utility = expValue(state.generateSuccessor(ghost_id, action), depth, next_ghost_id)
        # This is the only line that differs from the minValue used in Minimax. 
        # As an exp node in a game tree being explored by the Pacman, it has to
        # calculate the expectation using the probabilities previously calculated.
        expectation += action_probabilities[action] * utility

      return expectation
    
    actions = [ action for action in gameState.getLegalActions() if action != Directions.STOP ]
    actions_utilities = []
    for action in actions:
      actions_utilities.append((expValue(gameState.generateSuccessor(0, action), 1), action))
      
    best_action = max(actions_utilities)

    #print "LEGAL ACTIONS"
    #for a in actions_utilities:
    #  print "\t\t", a
    #print "BEST ONE:", best_action, "\n"

    return best_action[1]

def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function.
    
    DESCRIPTION: YARRRRR-READ AHOY
  """
  if currentGameState.isWin():  return float("inf")
  if currentGameState.isLose(): return float("-inf")
  
  # Fetch several data we require to analyze thecurrent state of the pacman's environment
  pacmanPos = currentGameState.getPacmanPosition()
  ghostStates = currentGameState.getGhostStates() 
  foodPos = currentGameState.getFood()
  capsules = currentGameState.getCapsules()

  def manhattan(xy1, xy2):
    "Our lil' and old Manhattan taxi drive distance function"
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])

  manhattans_food = [ ( manhattan(pacmanPos, food) ) for food in foodPos.asList() ]
  # For each of the manhattan distances to a food, we take the one
  # with the minimal distance possible
  min_manhattans_food = min(manhattans_food)

  manhattans_ghost = [ manhattan(pacmanPos, ghostState.getPosition()) for ghostState in ghostStates if ghostState.scaredTimer == 0 ]
  min_manhattans_ghost = -3
  # For each manhattan distance of a ghost, let's find the smalles distance possible.
  # Why an initial negative value? If no ghost exists in this state, simply give a
  # little price to Pacman for putting ghosts to rest.
  if ( len(manhattans_ghost) > 0 ): 
    min_manhattans_ghost = min(manhattans_ghost)

  manhattans_ghost_scared = [ manhattan(pacmanPos, ghostState.getPosition()) for ghostState in ghostStates if ghostState.scaredTimer > 0 ]
  min_manhattans_ghost_scared = 0;
  # The same goes with the scared ghosts. Find the smallest distance possible for each possible scared ghost.
  if ( len(manhattans_ghost_scared) > 0 ): 
    min_manhattans_ghost_scared = min(manhattans_ghost_scared)

  score = scoreEvaluationFunction(currentGameState)
  # The main objective of the pacman: THE PELLET. It has to be its utmost priority.
  score += -1.5 * min_manhattans_food
  # Why the inverse of the lowest distance possible? Pretty obvious, we want to
  # give the less points possible when a ghost is getting near the Pacman.
  score += -2 * ( 1.0 / min_manhattans_ghost )
  # So for scared ghosts, we give them the same weight as the normal ghosts,
  # though when we can eat them, they will be a pretty and tasty meal.
  score += -2 * min_manhattans_ghost_scared
  # Why this massive weight compared to other factors? We want the Pacman to be
  # focused on eating pellets, not capsules and then go for ghosts.
  score += -20 * len(capsules)
  # For each non eaten pellet, diminish current state score. It is important to
  # make the Pacman be enticed to go for pellets.
  score += -4 * len(foodPos.asList())

  return score

# Abbreviation
better = betterEvaluationFunction
