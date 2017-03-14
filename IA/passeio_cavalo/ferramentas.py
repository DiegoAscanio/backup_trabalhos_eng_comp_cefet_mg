import pdb

'''
    necessito de uma funcao que retorne uma tupla correspondente a um numero de
    casa
    entradas: c - numero da casa
              n - raiz quadrada do numero de casas do tabuleiro
    saida: j, k - tupla correspondente a casa
'''
def int_to_tuple(c, n):
    i = 1
    for j in range(1, n+1):
        for k in range(1, n+1):
            if i == c:
                return j, k
            i = i + 1

'''
    necessito de uma funcao que retorne um numero de casa correspondente a uma 
    tupla
    entradas: t - tupla correspondente a casa
              n - raiz quadrada do numero de casas do tabuleiro
    saida: numero correspondente a casa
'''
def tuple_to_int(t, n):
    i, j = t
    return int(i*n - (n-j))

'''
    necessito de uma funcao que calcule todas as adjacencias legais (casas ao 
    redor) de uma determinada casa do tabuleiro
    entrada: c - casa a ser verificada
             n - raiz quadrada do numero de casas do tabuleiro
    saida: legais - adjacencias possiveis de uma casa c
'''
def adjacencias(c, n):
    l, c = int_to_tuple(c, n)

    legais = []
    # adicionando todas as possibilidades de adjacencias da casa
    todas_adjacencias = [(l,c-1),(l-1,c),(l,c+1),(l+1,c)]
    for a in todas_adjacencias:
        # uma adjacencia e legal se 0 <= linha e coluna <= n
        l, c = a
        if l >= 1 and l <= n and c >= 1 and c <= n:
            legais.append(tuple_to_int(a, n))
    return legais

''' 
    necessito de uma funcao que calcule as movimentos legais para o movimento
    do cavalo a partir de uma determinada casa do tabuleiro
    entrada: c - casa a ser verficada
             n - raiz quadrada do numero de casas do tabuleiro
    saida: legais - movimentos legais que o cavalo pode realizar a partir da 
    casa c
'''
def movimentos_legais_cavalo(c, n):
    l, c = int_to_tuple(c, n)

    legais = []
    # adicionando todas as possibilidades de movimentos do cavalo
    todos_movimentos = [(l-1,c-2),(l-2,c-1),(l-2,c+1),(l-1,c+2),\
                         (l+1,c+2),(l+2,c+1),(l+2,c-1),(l+1,c-2)]
    # inspecionando possibilidades para verificar legalidade
    for m in todos_movimentos:
        # um movimento e legal se 0 <= linha e coluna <= n
        l, c = m
        if l >= 1 and l <= n and c >= 1 and c <= n:
            legais.append(tuple_to_int(m, n))
    return legais

'''
    necessito de uma funcao que gere um dicionario que mapeie casas para suas 
    movimentos legais, que correspondem aos movimentos possiveis de um cava
    lo dado que ele se encontra em determinada casa
    tal estrutura de dados e necessaria para a utilizacao em passos posterio
    res na construcao de funcao de avaliacao de utlidade de individuos para
    a selecao no algoritmo genetico
    entrada: n - raiz quadrada do numero de casas do tabuleiro
    saida: dicionario - dicionario mapeando movimentos validos para o cavalo
           em cada casa do tabuleiro
'''
def dicionario_movimentos_legais_cavalo(n):
    dicionario = {}
    for c in range(1,n**2 + 1):
        dicionario[c] = movimentos_legais_cavalo(c,n)
    return dicionario
