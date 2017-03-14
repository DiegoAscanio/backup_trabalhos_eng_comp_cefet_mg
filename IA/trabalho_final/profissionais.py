import random

'''
    Trabalho pratico de Inteligencia Artificial
    Utilizando um grafo representando uma rede social onde os vertices sao 
    individuos e as arestas representam amizades existentes entre os indi-
    viduos, a funcao profissionais retorna uma lista de pessoas que exer-
    cem uma determinada profissao a partir da lista de amigos de um indivi
    duo dessa rede social, procurando no maximo ate o segundo nivel alcan-
    cavel a partir desse individuo, onde alcancaria uma pessoa com um ami-
    go em comum. Isso e definido em saltos=2 por padrao, mas pode ser alte-
    rado, a criterio do fregues.

    Essa solucao visa facilitar o encontro de prestadores de servicos que
    possamos ter certa confianca e por isso, o nivel 2 - amigo do amigo.

    Esse trabalho e baseado em uma ideia proposta pelo professor de Otimi-
    zacao 2 - Fabio Rocha da Silva que sugeriu essa ideia em sala de aula
    como potencial facilitadora da vida moderna. E ela pode ser implementa-
    da utilizando-se busca de profundidade limitada em grafos, vista 
    na disciplina de Inteligencia Artifical, atendendo assim o enunciado
    do ultimo trabalho pratico da disciplina, que pediu ao aluno para so-
    lucionar um problema pratico (do cotidiano) usando algum dos conteudos
    vistos em sala de Aula.
'''

criterio = lambda u, profissao: u.profissao == profissao

def profissionais(g, individuo, profissao, saltos=2, criterio=criterio ):
    candidatos = []
    pilha = [individuo] # inicia pilha com individuo inicial e seu nivel
    backtrack = [(None, 0)]
    visitados = [] # lista de individuos visitados
    while len(pilha) > 0:
        u = pilha.pop()
        antecessor, nivel_corrente = backtrack.pop()

        if criterio(u, profissao): # se u possuir profissao desejada
            candidatos.append((u, antecessor, nivel_corrente))

        if u not in visitados:
            visitados.append(u)
            # para impedir a busca de ultrapassar o limite de saltos
            if nivel_corrente < saltos:
                for v in g[u]:
                    if v not in visitados and v not in pilha:
                        pilha.append(v)
                        backtrack.append((u, nivel_corrente + 1))
    return candidatos

class Individuo:
    def __init__(self, individuo_id, profissao):
        self.individuo_id = individuo_id
        self.profissao = profissao
    def __str__(self):
        return str(self.individuo_id)
    __repr__ = __str__

# dicionario de profissoes possiveis:
profissoes = {\
    1: 'advogado',\
    2: 'eletricista',\
    3: 'engenheiro',\
    4: 'medico',\
    5: 'gari'}

# dicionario de profissoes:
profissoes = {\
    1: 'advogado',\
    2: 'eletricista',\
    3: 'engenheiro',\
    4: 'medico',\
    5: 'gari',\
    6: 'jardineiro',\
    7: 'motorista',\
    8: 'enfermeiro',\
    9: 'secretario',\
    10: 'pedreiro',\
    11: 'bancario',\
    12: 'metalurgico',\
    13: 'estudante',\
    14: 'professor',\
    15: 'pesquisador'}

# definicao da lista de individuos para simulacao da rede social
# a rede social contara com 20 usuarios com profissoes aleatorias
# entre 5 definidas acima inicialmente
individuos = [Individuo(1, 3),\
              Individuo(2, 2),\
              Individuo(3, 3),\
              Individuo(4, 5),\
              Individuo(5, 5),\
              Individuo(6, 1),\
              Individuo(7, 5),\
              Individuo(8, 1),\
              Individuo(9, 4),\
              Individuo(10, 5),\
              Individuo(11, 4),\
              Individuo(12, 1),\
              Individuo(13, 5),\
              Individuo(14, 5),\
              Individuo(15, 3),\
              Individuo(16, 5),\
              Individuo(17, 1),\
              Individuo(18, 5),\
              Individuo(19, 3),\
              Individuo(20, 2)]

# simulacao da rede social
# a rede social sera simulada em um grafo sob a estrutura de dados dict
# de python

'''
rede_social = {i: [] for i in individuos}

for i in individuos:
    amigos = random.sample(individuos[0:individuos.index(i)]+\
                            individuos[individuos.index(i)+1:],\
                             random.randint(1,3))
    for j in amigos:
        if j not in rede_social[i]:
            rede_social[i].append(j)
            rede_social[j].append(i)
'''

# rede social bem definida ja visualizada e testada, apta para testes
rede_social = {individuos[4]: [individuos[13], individuos[1], individuos[16], individuos[17], individuos[19]],\
               individuos[0]: [individuos[16], individuos[19]],\
               individuos[8]: [individuos[7], individuos[6], individuos[13], individuos[16]],\
               individuos[19]: [individuos[0], individuos[10], individuos[6], individuos[4]],\
               individuos[9]: [individuos[5], individuos[14]],\
               individuos[15]: [individuos[3], individuos[7], individuos[13]],\
               individuos[10]: [individuos[2], individuos[3], individuos[19]],\
               individuos[16]: [individuos[0], individuos[6], individuos[7], individuos[8], individuos[4], individuos[17]],\
               individuos[11]: [individuos[1], individuos[12], individuos[3], individuos[18]],\
               individuos[13]: [individuos[1], individuos[4], individuos[8], individuos[15]],\
               individuos[6]: [individuos[16], individuos[12], individuos[8], individuos[19]],\
               individuos[1]: [individuos[11], individuos[13], individuos[4]],\
               individuos[2]: [individuos[10]],\
               individuos[18]: [individuos[11], individuos[14], individuos[7]],\
               individuos[12]: [individuos[5], individuos[6], individuos[11], individuos[7]],\
               individuos[7]: [individuos[15], individuos[16], individuos[8], individuos[12], individuos[18]],\
               individuos[14]: [individuos[5], individuos[9], individuos[18]],\
               individuos[3]: [individuos[15], individuos[10], individuos[11]],\
               individuos[17]: [individuos[16], individuos[4]],\
               individuos[5]: [individuos[9], individuos[12], individuos[14]]}

# imprime no formato da biblioteca de grafos

for i in individuos:
    print("    {id: %d, label: \'Ind. %d - %s\'},"%(i.individuo_id, i.individuo_id, profissoes[i.profissao]))

for i in rede_social:
    for j in rede_social[i]:
        print("    {from: %s, to: %s},"%(i, j))
