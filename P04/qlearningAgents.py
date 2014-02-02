# -*- coding: utf-8 -*-

from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math
          
class QLearningAgent(ReinforcementAgent):
  """
  Q-Learning Agent
  
  Functions you should fill in:
  
    - `getQValue`
    - `getAction`
    - `getValue`
    - `getPolicy`
    - `update`
    
  Instance variables you have access to
  
    - `self.epsilon` (exploration prob)
    - `self.alpha` (learning rate)
    - `self.gamma` (discount rate)
  
  Functions you should use
  
    - `self.getLegalActions(state)` Returns legal actions for a state
  """
  def __init__(self, **args):
    """
    You can initialize Q-values here...
    """
    ReinforcementAgent.__init__(self, **args)
    self.Q = util.Counter()
    # Modify this value to set how many actions to choose randomly before selecting greedily
    self.greedy_constraint = 100
    self.to_greedy = 0
  
  def getQValue(self, state, action):
    """
    Returns Q(state,action). Should return `0.0` if we never have seen a state or (state,action) tuple.
    """
    if (state, action) not in self.Q:
      return 0.0
    else:
      return self.Q[(state, action)]
    
  def getValue(self, state):
    """
    Returns `max(Q(state,action))`.

    Where the max is over legal actions.  Note that if
    there are no legal actions, which is the case at the
    terminal state, you should return a value of `0.0`.
    """
    actions = self.getLegalActions(state)
    if not actions:
      return 0.0
    return max([ self.getQValue(state, action) for action in actions ])
    
  def getPolicy(self, state):
    """
    Compute the best actions to take in a state.  Note that if there
    are no legal actions, which is the case at the terminal state,
    you should return None.
    """
    actions = self.getLegalActions(state)
    if not actions:
      return None

    q_actions = [ (self.getQValue(state, action), action) for action in actions ]
    qa = max(q_actions, key = lambda x: x[0])
    return qa[1]
    
  def getAction(self, state):
    """
    Compute the action to take in the current state.  With
    probability self.epsilon, we should take a random action and
    take the best policy action otherwise.  Note that if there are
    no legal actions, which is the case at the terminal state, you
    should choose None as the action.
  
    `HINT`: You might want to use `util.flipCoin(prob)`
    
    `HINT`: To pick randomly from a list, use `random.choice(list)`
    """  
    action = None
    actions = self.getLegalActions(state)

    if actions:
      if util.flipCoin(self.epsilon):
        action = random.choice(actions)
      else:
        action = self.getPolicy(state)
    
    return action
  
  def update(self, state, action, nextState, reward):
    """
    The parent class calls this to observe a 
    state = action => nextState and reward transition.
    You should do your Q-Value update here
    
    `NOTE`: You should never call this function, it will be called on your behalf

    `NOTE`:
      
      > state     = s
      > nextState = s'
      > action    = a
      > reward    = r'
    """
    sample = reward
    pair = (state, action)
    sample = reward + ( self.gamma * self.getValue(nextState) )
    self.Q[pair] = ( ( 1 - self.alpha ) * self.Q[pair] ) + ( self.alpha * sample )
    
class PacmanQAgent(QLearningAgent):
  """
  Exactly the same as QLearningAgent, but with different default parameters
  """
  
  def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
    """
    These default parameters can be changed from the pacman.py command line.
    For example, to change the exploration rate, try:
    
    `python pacman.py -p PacmanQLearningAgent -a epsilon=0.1`
    
    `alpha`    - learning rate
    
    `epsilon`  - exploration rate
    
    `gamma`    - discount factor
    
    `numTraining` - number of training episodes, i.e. no learning after these many episodes
    """
    args['epsilon'] = epsilon
    args['gamma'] = gamma
    args['alpha'] = alpha
    args['numTraining'] = numTraining
    QLearningAgent.__init__(self, **args)

  def getAction(self, state):
    """
    Simply calls the getAction method of `QLearningAgent` and then
    informs parent of action for Pacman.  Do not change or remove this
    method.
    """
    action = QLearningAgent.getAction(self,state)
    self.doAction(state,action)
    return action

    
class ApproximateQAgent(PacmanQAgent):
  """
  You should only have to overwrite `getQValue`
  and `update`.  All other `QLearningAgent` functions
  should work as is.
  """
  def __init__(self, extractor='IdentityExtractor', **args):
    PacmanQAgent.__init__(self, **args)
    self.featExtractor = util.lookup(extractor, globals())()
    self.weights = util.Counter()
    
  def getQValue(self, state, action):
    """
    Should return Q(state,action) = w * featureVector
    where * is the dotProduct operator
    """
    features = self.featExtractor.getFeatures(state, action)
    return sum([ value * self.weights[feature] for feature, value in features.iteritems() ])
    
  def update(self, state, action, nextState, reward):
    """
    Should update your weights based on transition  
    """
    features = self.featExtractor.getFeatures(state, action)
    for feature, value in features.iteritems():
      correction = ( reward + ( self.gamma * self.getValue(nextState) ) ) - self.getQValue(state, action)
      self.weights[feature] += self.alpha * correction * value
    
  def final(self, state):
    """
    Called at the end of each game.
    """
    # call the super-class final method
    PacmanQAgent.final(self, state)
    
    # did we finish training?
    if self.episodesSoFar == self.numTraining:
      pass
