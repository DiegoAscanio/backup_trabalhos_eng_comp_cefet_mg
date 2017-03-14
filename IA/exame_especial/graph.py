import pdb
import heapq

graph = {1: [2, 5, 6], 2: [1, 3, 4], 3: [2, 7], 4: [2, 10], 5: [1, 11, 12], 6: [1, 12], 7: [3, 8, 9], 8: [7], 9: [7], 10: [4], 11: [5], 12: [5, 6]}

# pesos das arestas - necessario para a estrela
weights = {(1, 2): 2,
           (1, 5): 1,
           (1, 6): 4,
           (2, 1): 2,
           (2, 3): 1,
           (2, 4): 3,
           (3, 2): 1,
           (3, 7): 2,
           (4, 2): 3,
           (4, 10): 1,
           (5, 1): 1,
           (5, 11): 2,
           (5, 12): 8,
           (6, 1): 4,
           (6, 12): 4,
           (7, 3): 2,
           (7, 8): 5,
           (7, 9): 2,
           (8, 7): 5,
           (9, 7): 2,
           (10, 4): 1,
           (11, 5): 2,
           (12, 5): 8,
           (12, 6): 4}

coordinates = {1: (0, 0),
               2: (0, 1),
               3: (0, 2),
               4: (-1, 1),
               5: (1, 0),
               6: (2, 2),
               7: (1, 2),
               8: (3, 4),
               9: (1, 4),
               10: (-1, 0),
               11: (1, -1),
               12: (6, 2)}

# heuristica para o a estrela
heuristic = lambda a, b: abs(a[0] - b[0]) + abs(a[1] - b[1])

# questao 3
# busca em aprofundamento iterativo

def aprofundamento_iterativo (graph, start_node, solution_node, depth=1, max_iter=100):
    # funcionamento da busca de aprofundamento iterativo:
    # aumenta o tamanho da profundidade da arvore a partir de uma
    # profundidade minima depth ate um numero maximo de iteracoes
    # max_iter
    # a busca funciona sempre buscando o filho mais a direita de
    # um no. Quando a profundidade minima escolhida nao abrange o
    # no objetivo da arvore, na proxima iteracao, como nao e nece-
    # ssario revisitar os nos ja visitados da arvore, a visitacao
    # comecara a partir do ultimo no inserido (no filho mais a es
    # querda da sub-arvore de profundidade escolhida. E os filhos
    # dele serao adicionados da mesma maneira anterior, sempre os
    # mais a direita, assim como nos outros nos filhos de mesmo
    # nivel

    # funcao para calcular profundidade de um no
    node_depth = lambda x: 0 if x == start_node else 1 + node_depth(graph[x][0])

    visiteds = [] # lista dos nos visitados
    stack = [start_node] # pilha de exploracao
    
    current_node = start_node

    i = depth
    while i <= max_iter: 
        stack_next_depth = []
        while stack and current_node != solution_node:
            current_node = stack.pop()
            if current_node not in visiteds:
                visiteds.append(current_node)
            for s in graph[current_node]:
                stack.append(s) if s not in visiteds and node_depth(s) <= i else stack_next_depth.append(s)
        stack = stack_next_depth
        i += 1
    return visiteds

def a_estrela(graph, start_node, solution_node):
    # funcionamento do a*:
    # o a estrela funciona utilizando memorizacao dos custos de 
    # caminhos, o que evita loops e pelo fato de utilizar uma
    # heuristica otimista (distancia de manhattan), associada a 
    # uma fila de prioridades, ele ao explorar novos caminhos,
    # sempre vai tender a assumir o que mais rapido alcanca o o
    # bjetivo do problema
    priority_queue = [] # fila de prioridades
    # construida usando heaps - nota-se a prioridade no heapq
    # do python da-se por uma tupla (prioridade, objeto)
    heapq.heappush(priority_queue, (0, start_node))
    path = {}
    path_weight = {}
    path[start_node] = None
    path_weight[start_node] = 0
    while priority_queue:
        # o 2o elemento da tupla, retirada da fila de prioridades
        current_node = heapq.heappop(priority_queue)[1]
        if current_node == solution_node: # solucao encontrada
            break
        for s in graph[current_node]: # adjacencias do no corrente
            # novo peso calculado a partir do dicionario de pesos
            new_weight = path_weight[current_node] + weights[(current_node, s)]
            if s not in path_weight or new_weight < path_weight[s]:
                path_weight[s] = new_weight
                # atuacao da heuristica
                priority = new_weight + heuristic(coordinates[solution_node], coordinates[s])
                heapq.heappush(priority_queue, (priority, s))
                path[s] = current_node
    return path[current_node], path_weight[current_node]

# prezado flavio, voce vai receber via e-mail uma foto do grafo
# com arestas, suas coordenadas e seus respectivos pesos
# o a estrela foi testado para ir do no 1 ao 12 do grafo
# e o caminho minimo previsto e o que passa pelo no 6 com custo 8
# o algoritmo foi implementado corretamente, pois ao testar para
# essas entradas:
# a_estrela(graph,1,12)
# os valores encontrados foram: (6, 8)
