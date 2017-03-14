# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
"""

import util
import pdb

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

def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first [p 85].
  
  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm [Fig. 3.7].
  
  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:
  
  print "Start:", problem.getStartState()
  print "Is the start a goal?", problem.isGoalState(problem.getStartState())
  print "Start's successors:", problem.getSuccessors(problem.getStartState())
  """
  "*** YOUR CODE HERE ***"


  # exploracao: uma pilha de tuplas contendo estados e listas de acoes
  # necessarias para se alcancar um estado
  exploracao = util.Stack()

  # estadosVisitados - uma lista contendo os estados visitados
  estadosVisitados = []

  # estadoCorrente - variavel a ser atualizada no while
  # incialmente e o estado inicial
  estadoCorrente = problem.getStartState()
  
  # acoes - lista de acoes a ser executadas para se alcancar o estado
  # objetivo
  acoes = []

  while not problem.isGoalState(estadoCorrente):
    if estadoCorrente not in estadosVisitados: # remocao do loop
      estadosVisitados.append(estadoCorrente)
    for e, a, s in problem.getSuccessors(estadoCorrente):
      if e not in estadosVisitados:
        exploracao.push((e, acoes + [a]))
    estadoCorrente, acoes = exploracao.pop()

  return acoes # o ultimo estado corrente e o objetivo, juntamente com 
               # a ultima acao corrente
  

def breadthFirstSearch(problem):
  "Search the shallowest nodes in the search tree first. [p 81]"
  "*** YOUR CODE HERE ***"
  # exploracao: uma filha de tuplas contendo estados e listas de acoes
  # necessarias para se alcancar um estado
  # problem.getStartState () e o estado inicial e a lista de acoes ini
  # cial e vazia (como esperado)
  exploracao = util.Queue()

  # estadosVisitados - uma lista contendo os estados visitados
  estadosVisitados = []

  # segundo cormen - enqueue s (Start State) in Q
  # a lista vazia representa as acoes necessarias para
  # se alcancar o estado inicial
  exploracao.push((problem.getStartState(),[]))

  while not exploracao.isEmpty():
    estadoCorrente, acoes = exploracao.pop()
    for e, a, s in problem.getSuccessors(estadoCorrente):
      if e not in estadosVisitados:
        # Quando o estado objetivo e alcancado, retorna-se as
        # acoes que o levaram a chegar ali
        if problem.isGoalState(e):
          return acoes + [a]
        # adiciona-se o ultimo estado explorado e as acoes
        # necessarias para chegar ate ele na fila de exploracao
        exploracao.push((e, acoes + [a]))
        estadosVisitados.append(e)
    estadosVisitados.append(estadoCorrente)

  return []

def uniformCostSearch(problem):
  "Search the node of least total cost first. "
  "*** YOUR CODE HERE ***"
  # exploracao: uma filha de prioridades de tuplas contendo estados e listas
  # de acoes necessarias para se alcancar um estado.
  # problem.getStartState () e o estado inicial e a lista de acoes inicial 
  # e vazia (como esperado)
  exploracao = util.PriorityQueue()

  # estadosVisitados - uma lista contendo os estados visitados
  estadosVisitados = []

  # segundo cormen - enqueue s (Start State) in Q
  # a lista vazia representa as acoes necessarias para
  # se alcancar o estado inicial
  exploracao.push((problem.getStartState(),[]), 0)

  while not exploracao.isEmpty():
    estadoCorrente, acoes = exploracao.pop()
    for e, a, s in problem.getSuccessors(estadoCorrente):
      if e not in estadosVisitados:
        # Quando o estado objetivo e alcancado, retorna-se as
        # acoes que o levaram a chegar ali
        if problem.isGoalState(e):
          return acoes + [a]
        # adiciona-se o ultimo estado explorado e as acoes
        # necessarias para chegar ate ele na fila de exploracao
        # o custo na busca de custo uniforme e dado pelo custo para se chegar 
        # as acoes
        exploracao.push((e, acoes + [a]), problem.getCostOfActions(acoes + [a]))
        estadosVisitados.append(e)
    estadosVisitados.append(estadoCorrente)

  return []


def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  "*** YOUR CODE HERE ***"
  # exploracao: uma filha de prioridades de tuplas contendo estados e listas
  # de acoes necessarias para se alcancar um estado.
  # problem.getStartState () e o estado inicial e a lista de acoes inicial 
  # e vazia (como esperado)
  exploracao = util.PriorityQueue()

  # estadosVisitados - uma lista contendo os estados visitados
  estadosVisitados = []

  # segundo cormen - enqueue s (Start State) in Q
  # a lista vazia representa as acoes necessarias para
  # se alcancar o estado inicial
  exploracao.push((problem.getStartState(),[]), 0)

  while not exploracao.isEmpty():
    estadoCorrente, acoes = exploracao.pop()
    for e, a, c in problem.getSuccessors(estadoCorrente):
      if e not in estadosVisitados:
        # Quando o estado objetivo e alcancado, retorna-se as
        # acoes que o levaram a chegar ali
        if problem.isGoalState(e):
          return acoes + [a]
        # adiciona-se o ultimo estado explorado e as acoes
        # necessarias para chegar ate ele na fila de exploracao
        # o custo no a* e dado pelo custo para se executar as acoes mais o custo
        # oriundo da heuristica
        exploracao.push((e, acoes + [a]), problem.getCostOfActions(acoes + [a]) + heuristic(e, problem))
        estadosVisitados.append(e)
    estadosVisitados.append(estadoCorrente)

  return []
    
  
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
