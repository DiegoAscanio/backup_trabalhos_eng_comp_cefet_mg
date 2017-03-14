# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random, util
import pdb

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
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    oldFood = currentGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    "*** YOUR CODE HERE ***"
    
    compare = lambda ghost_1, ghost_2, pacman: -1 if util.manhattanDistance(pacman, ghost_1) - util.manhattanDistance(pacman, ghost_2) < 0 else 1 if util.manhattanDistance(pacman, ghost_1) - util.manhattanDistance(pacman, ghost_2) > 0 else 0
    oldFoodList = oldFood.asList()
    oldFoodList.sort(lambda x, y: util.manhattanDistance(newPos, x)-util.manhattanDistance(newPos, y))
    foodScore = util.manhattanDistance(newPos, oldFoodList[0])
    ghostPositions = [g.getPosition() for g in newGhostStates]

    if len(ghostPositions) == 0:
        ghostScore = 0
    else:
        ghostPositions.sort(lambda x, y: compare(x,y,newPos))
        if util.manhattanDistance(newPos, ghostPositions[0]) == 0:
            return -99
        else:
            ghostScore = -2./util.manhattanDistance(newPos, ghostPositions[0])
    return 2. + ghostScore if foodScore == 0 else ghostScore + 1./float(foodScore)

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

  def minimax (self, numOfAgents, agentIndex, gameState, depth):
    if gameState.isLose() or gameState.isWin() or depth == 0: # teste de termino
        return self.evaluationFunction(gameState) # utilidade
    else:
        nextStates = [gameState.generateSuccessor(agentIndex,action) for action in gameState.getLegalActions(agentIndex)]
        return max([self.minimax(numOfAgents,(agentIndex+1)%numOfAgents,nextState,depth-1) for nextState in nextStates]) if agentIndex == 0 else min([self.minimax(numOfAgents,(agentIndex+1)%numOfAgents,nextState,depth-1) for nextState in nextStates])

  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction.

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    "*** YOUR CODE HERE ***"
    numOfAgents = gameState.getNumAgents()
    depth = numOfAgents*self.depth # a profundidade da arvore de decisoes e intrinsicamente ligada ao numero de agentes jogando
    legalActions = gameState.getLegalActions(0) # movimentos validos para o pacman - agent id 0

    if Directions.STOP in legalActions:
        legalActions.remove(Directions.STOP) # remove a acao de permanecer parado

    nextStates = [gameState.generateSuccessor(0,action) for action in legalActions] # proximos sucessores otimos do pacman para cada acao legal valida
    values = [self.minimax(numOfAgents,1,nextState,depth-1) for nextState in nextStates] # calcula os valores minimax para cada acao
    Max = max(values) # pega o ganho maximo das acoes
    listMax = [i for i in range(0,len(values)) if values[i] == Max] # constroi uma lista de acoes com ganhos maximos
    return legalActions[random.choice(listMax)] # retorna uma acao aleatoria de ganho maximo para ser executada

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """
  INF = 10**10
  def minimax (self, numOfAgents, agentIndex, gameState, depth, alfa=-INF, beta=INF):
    if gameState.isLose() or gameState.isWin() or depth == 0: # teste de termino
        return self.evaluationFunction(gameState) # utilidade
    else:
        nextStates = [gameState.generateSuccessor(agentIndex,action) for action in gameState.getLegalActions(agentIndex)]
        if agentIndex == 0: # max
            v = -self.INF
            v = max([self.minimax(numOfAgents, (agentIndex + 1)%numOfAgents, nextState, depth - 1, alfa, beta) for nextState in nextStates])
            if v < beta:
                alfa = max(alfa,v)
            return v
        else: # min
            v = self.INF
            v = min([self.minimax(numOfAgents, (agentIndex + 1)%numOfAgents, nextState, depth - 1, alfa, beta) for nextState in nextStates])
            if v > alfa:
                beta = max(beta,v)
            return v


  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"
    numOfAgents = gameState.getNumAgents()
    depth = numOfAgents*self.depth # a profundidade da arvore de decisoes e intrinsicamente ligada ao numero de agentes jogando
    legalActions = gameState.getLegalActions(0) # movimentos validos para o pacman - agent id 0

    if Directions.STOP in legalActions:
        legalActions.remove(Directions.STOP) # remove a acao de permanecer parado

    nextStates = [gameState.generateSuccessor(0,action) for action in legalActions] # proximos sucessores otimos do pacman para cada acao legal valida
    values = [self.minimax(numOfAgents,1,nextState,depth-1) for nextState in nextStates] # calcula os valores minimax para cada acao
    Max = max(values) # pega o ganho maximo das acoes
    listMax = [i for i in range(0,len(values)) if values[i] == Max] # constroi uma lista de acoes com ganhos maximos
    return legalActions[random.choice(listMax)] # retorna uma acao aleatoria de ganho maximo para ser executada

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (question 4)
  """
  def expectimax(self, numOfAgents, agentIndex, gameState, depth):
    if gameState.isLose() or gameState.isWin() or depth == 0: # teste de termino
        return self.evaluationFunction(gameState) # utilidade
    else:
        nextStates = [gameState.generateSuccessor(agentIndex,action) for action in gameState.getLegalActions(agentIndex)]
        chanceList = [self.expectimax(numOfAgents,(agentIndex+1)%numOfAgents,nextState,depth-1) for nextState in nextStates]
        return max([self.expectimax(numOfAgents,(agentIndex+1)%numOfAgents,nextState,depth-1) for nextState in nextStates]) if agentIndex == 0 else sum(chanceList)/len(chanceList)

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """
    "*** YOUR CODE HERE ***"
    numOfAgents = gameState.getNumAgents()
    depth = numOfAgents*self.depth
    legalActions = gameState.getLegalActions(0) # movimentos validos para o pacman - agent id 0

    if Directions.STOP in legalActions:
        legalActions.remove(Directions.STOP) # remove a acao de permanecer parado

    nextStates = [gameState.generateSuccessor(0,action) for action in legalActions] # proximos sucessores otimos do pacman para cada acao legal valida
    values = [self.expectimax(numOfAgents,1,nextState,depth-1) for nextState in nextStates] # calcula os valores minimax para cada acao
    Max = max(values) # pega o ganho maximo das acoes
    listMax = [i for i in range(0,len(values)) if values[i] == Max] # constroi uma lista de acoes com ganhos maximos
    return legalActions[random.choice(listMax)] # retorna uma acao aleatoria de ganho maximo para ser executada


def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
  """
  "*** YOUR CODE HERE ***"
  util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

