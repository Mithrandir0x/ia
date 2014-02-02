import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
  """
  A ValueIterationAgent takes a Markov decision process
  (see mdp.py) on initialization and runs value iteration
  for a given number of iterations using the supplied
  discount factor.
  """
  def __init__(self, mdp, discount = 0.9, iterations = 100):
    """
    Your value iteration agent should take an mdp on
    construction, run the indicated number of iterations
    and then act according to the resulting policy.
    
    Some useful mdp methods you will use:
        
        mdp.getStates()
        mdp.getPossibleActions(state)
        mdp.getTransitionStatesAndProbs(state, action)
        mdp.getReward(state, action, nextState)
    """
    self.mdp = mdp
    self.discount = discount
    self.iterations = iterations
    # A Counter is a dict with default 0
    self.values = util.Counter()
    
    self.qvalues = { state: {} for state in states }
    self.policy = { state: None for state in states }

    states = mdp.getStates()
    for i in xrange(  1, iterations + 1):
      for state in states:
        actions = mdp.getPossibleActions(state)
        v = []
        for action in actions:
          # Given each possible action in the current state, calculate all the
          # possible values we could obtain by using Bellman's equation
          t = mdp.getTransitionStatesAndProbs(state, action)
          k = [ p * ( mdp.getReward(state, action, nextState) + ( discount * self.values[(i - 1, nextState)] ) ) for nextState, p in t ]
          q = sum(k)
          self.qvalues[state][action] = q
          v.append([q, action])
        if len(v) > 0:
          q, action = max(v, key = lambda x: x[0])
          self.values[(i, state)] = q
          self.policy[state] = action
    
  def getValue(self, state):
    """
    Return the value of the state (computed in `__init__`).
    """
    return self.values[(self.iterations, state)]


  def getQValue(self, state, action):
    """
    The q-value of the state action pair
    (after the indicated number of value iteration
    passes).  Note that value iteration does not
    necessarily create this quantity and you may have
    to derive it on the fly.
    """
    return self.qvalues[state][action]

  def getPolicy(self, state):
    """
    The policy is the best action in the given state
    according to the values computed by value iteration.
    You may break ties any way you see fit.  Note that if
    there are no legal actions, which is the case at the
    terminal state, you should return `None`.
    """
    return self.policy[state]

  def getAction(self, state):
    """
    Returns the policy at the state (no exploration).
    """
    return self.getPolicy(state)
  
