# AG para resolucao problema n rainhas

import numpy
import sys
import itertools
import random
import copy
import math
import pdb
import getopt

# definicao de uma funcao fatorial
fat = lambda x: 1 if x < 2 else x*fat(x-1)

# definicao da funcao de fitness - pares de rainhas que nao se atacam

def fitness (i):
    tabuleiro = list(i)
    pares = len(tabuleiro) ** 2
    coluna_corrente = 0
    while coluna_corrente < len(tabuleiro):
        linha_corrente = tabuleiro[coluna_corrente]
        coluna_adjacencia = 0
        for linha_adjacencia in tabuleiro:
            try:
                m = math.fabs(float(coluna_adjacencia - coluna_corrente)/float(linha_adjacencia - linha_corrente))
            except ZeroDivisionError:
                m = 'inf'
            if m == 0. or m == 1. or m == 'inf':
                pares -= 1
            coluna_adjacencia += 1
        coluna_corrente += 1
    return pares

def calcula_posicao_roleta (probabilidade):
    global probabilidade_corrente
    probabilidade_corrente += probabilidade
    return probabilidade_corrente


def ag (n, tamanho_individuos, individuos, geracoes, probabilidade_mutacao, x=1, f=fitness):
    # execucao do algoritmo genetico
    g = 1
    solucao_final = False

    while g <= geracoes and not solucao_final:
        
        # prepara os individuos para pareamento
        random.shuffle(individuos)
        filhos = []
        # cruzamento
        for i in range(0,len(individuos)-1,2):
            # estrategia ox
            filho_1 = [-1 for j in range(0,n)]
            filho_2 = [-1 for j in range(0,n)]
            start = random.randint(0, n - 2)
            finish = 1 if start == n - 2 else random.randint(1, n - start - 1)
            filho_1[start:start+finish] = individuos[i][start:start+finish]
            filho_2[start:start+finish] = individuos[i+1][start:start+finish]
            not_filho_1 = [individuos[i+1][j] for j in range(0,n) if individuos[i+1][j] not in filho_1]
            not_filho_2 = [individuos[i][j] for j in range(0,n) if individuos[i][j] not in filho_2]
            for j in range(0,n):
                if filho_1[j] == -1:
                    filho_1[j] = not_filho_1.pop(0)
                if filho_2[j] == -1:
                    filho_2[j] = not_filho_2.pop(0)
            
            if random.random() < probabilidade_mutacao:      
                filho_1[start],filho_1[start+finish]=filho_1[start+finish],filho_1[start]
                filho_2[start],filho_2[start+finish]=filho_2[start+finish],filho_2[start]

            filhos.append(filho_1)
            filhos.append(filho_2)

        # realiza selecao - por roleta
        individuos += filhos
        novos_individuos = []
        fitness_individuos = map(f,individuos)
        fitness_total = sum(fitness_individuos)
        probabilidades_individuais = map(lambda x: float(x)/fitness_total, fitness_individuos)
        # chaves
        global probabilidade_corrente
        probabilidade_corrente = 0
        roleta = dict(zip(map(calcula_posicao_roleta,probabilidades_individuais),individuos))
        while len(novos_individuos) < tamanho_individuos:
            i = random.random()
            chaves = roleta.keys()
            chaves.sort()
            for k in chaves:
                if k >= i:
                    break
            novos_individuos.append(roleta[k])

        individuos = novos_individuos
        # verifica se ja alcancou solucao final
        individuos.sort(key=f,reverse=True)
        if fitness(individuos[0]) == n*(n-1):
            solucao_final = True

        g += 1

    return individuos[0:x]

def subida_encosta (s, N, f=fitness):
    vizinhanca = []
    for v in N:
        if f(v) >= f(s):
            vizinhanca.append(v)
    while len(vizinhanca) > 0:
        vizinhanca.sort(key=f,reverse=True)
        s = vizinhanca.pop(0)
        # redefinicao da vizinhanca
        N = copy.copy(vizinhanca)
        vizinhanca = []
        for v in N:
            if f(v) >= f(s):
                vizinhanca.append(v)
    return s

def main (argv):
    # definicao da solucao - 1 subida, 2 - ag, 3 - hibrido
    solucao = int(argv[0])
    # quantidade execucoes
    quantidade_execucoes = int(argv[1])
    # definicao do tamanho do tabuleiro - n
    n = int(argv[2])
    # definicao do tamanho da populacao inicial
    tamanho_populacao = int(argv[3])
    # definicao da quantidade de geracoes a se executar
    geracoes = int(argv[4])
    # definicao da probabilidade de mutacao
    probabilidade_mutacao = float(argv[5])
    # definicao da quantiade de individuos tops
    x = int(argv[6])

    # geracao de ate maximo_permutacoes ou n! permutacoes possiveis a partir do individuo:
    individuo_inicial = range(0,n)
    maximo_permutacoes = fat(n) if fat(n) <= fat(9) else 5000000*(1 - numpy.exp(-n/100))
    iterador_permutacoes = itertools.permutations(individuo_inicial)
    permutacoes = []

    if maximo_permutacoes >= fat(9) :
        i = 0
        while i < maximo_permutacoes:
            p = iterador_permutacoes.next()
            if random.randint(0,i) % random.randint(1,n*n) == 0:
                permutacoes.append(p)
                i += 1
    else:
        permutacoes = list(iterador_permutacoes)

    populacao = [list(random.choice(permutacoes)) for i in range(0,tamanho_populacao)]

    if solucao == 1: # subida encosta
        print ('Execucao\tIndividuo\tFitness')
        for i in range(0,quantidade_execucoes):
            s = list(random.choice(permutacoes))
            j = permutacoes.index(tuple(s))
            N = permutacoes[j-x:j+x]
            melhor_individuo = subida_encosta(individuo_inicial,N)
            print ('%d\t%s\t%d'% (i+1,melhor_individuo,fitness(melhor_individuo)))
    elif solucao == 2: # ag
        print ('Execucao\tIndividuo\tFitness')
        for i in range(0,quantidade_execucoes):
            melhor_individuo = ag(n,tamanho_populacao,copy.copy(populacao),geracoes,probabilidade_mutacao)
            print ('%d\t%s\t%d'% (i+1,melhor_individuo[0],fitness(melhor_individuo[0])))
    elif solucao == 3: # hibrido
        print ('Execucao,Individuo\tFitnessIndividuo\tMelhorIndividuo\tFitnessMelhorIndividuo')
        for i in range(0,quantidade_execucoes):
            individuos = ag(n,tamanho_populacao,copy.copy(populacao),geracoes,probabilidade_mutacao,x)
            for s in individuos:
                iterador_permutacoes = itertools.permutations(s)
                permutacoes = []
                for j in range (0,2*x):
                    permutacoes.append(iterador_permutacoes.next())
                random.shuffle(permutacoes)
                melhor_individuo = subida_encosta(s,permutacoes)
                print ('%d\t%s\t%d\t%s\t%d' % (i+1,s,fitness(s),melhor_individuo,fitness(melhor_individuo)))

if __name__ == "__main__":
    main(sys.argv[1:])
