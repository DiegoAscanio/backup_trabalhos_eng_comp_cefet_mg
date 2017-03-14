import ferramentas
import random
import pdb
from copy import deepcopy

def fitness(individuo):
    pass

class AlgoritmoGeneticoPasseioCavalo:
    """
        Classe que contem a implementacao de algoritmos geneticos para solucio-
        nar o problema do passeio de cavalo
    """
    def __init__(self, n, tamanho_populacao, geracoes, probabilidade_mutacao, fitness=None):
        """
            Construtor: 
            n = raiz quadrada do numero de casas do tabuleiro
            tamanho_populacao = quantidade de individuos a ser gerado na populacao
            geracoes = numero maximo de geracoes
            propabilidade_mutacao = probabilidade de uma mutacao ocorrer
            fitness = funcao fitness
        """
        self.n = n
        self.tamanho_individuo = n**2
        self.tamanho_populacao = tamanho_populacao
        self.geracoes = geracoes
        self.probabilidade_mutacao = probabilidade_mutacao
        self.fitness = fitness if fitness is not None else self.__fitness
        self.populacao = []
        self.descendentes = []
        self.valor_individuos = {}
        self.movimentos_legais = ferramentas.dicionario_movimentos_legais_cavalo(self.n)

    def __fitness(self, *args):
        """
            Uma funcao para calcular o quanto vale um determinado individuo da 
            populacao. Esse valor pode ser atribuido com a maior quantidade de
            movimentos legais que esse individuo possui
            Entrada: individuo
            Saida: aptidao
        """

        individuo = args[0]

        aptidao = 0
        aptidao_local = 0
        i = 0
        j = 0

        movimentos_legais = deepcopy(self.movimentos_legais)

        while i < len(individuo) - 1:
            j = i
            while j < len(individuo) - 1 and individuo[j + 1] \
                  in movimentos_legais[individuo[j]]:
                aptidao_local += 1
                if aptidao < aptidao_local:
                    aptidao = aptidao_local
                j += 1
            i = j + 1
            aptidao_local = 0

        return aptidao

    def __individuo_aleatorio(self):
        """ Usado para gerar individuos aleatorios - iniciar_populacao """
        individuo = [i for i in range(1, self.tamanho_individuo + 1)]
        random.shuffle(individuo)
        return tuple(individuo)

    def __individuo_aleatorio_disponiveis(self):
        """ 
            Usado para gerar individuos aleatorios escolhendo-se vizinhos
            disponiveis 
        """
        individuo_temporario = [i for i in range(1, self.tamanho_individuo + 1)]
        individuo = []

        c = random.choice(individuo_temporario)
        individuo.append(c)
        individuo_temporario.remove(c)

        while len(individuo_temporario) > 0:
            # assume-se que todos vizinhos estejam visitados para selecionar 
            # uma casa aleatoria de invididuo_temporario se necessario
            vizinhos_visitados = True
            adjacencias = ferramentas.adjacencias(c, self.n)
            for a in adjacencias:
                if a not in individuo:
                    vizinhos_visitados = False
                    c = a
                    break
            if vizinhos_visitados: # todos os vizinhos de c foram visitados
                c = random.choice(individuo_temporario)

            individuo.append(c) # adiciona uma casa valida pela regra
            individuo_temporario.remove(c) # remove da lista temporaria

        return tuple(individuo)

    def __individuo_warnsdorff(self):
        """
            Abordagem utilizada para warnsdorff:
            1. Gerar dicionario com todos os movimentos validos para um cavalo 
               em um tabuleiro - utilizando dicionario_movimentos_legais_cavalo
               contida em ferramentas
            2. Criar um individuo temporario 1->self.tamanho_individuo
            3. colher aleatoriamente uma casa desse individuo temporario
            5. colher a vizinhanca desta casa
            4. adicionar essa casa no individuo a ser retornado
            5. retirar a casa de todas as vizinhancas de casas dos movimentos
               validos
            6. colher de individuo temporario uma casa da vizinhanca colhida 
               seguindo o criterio de warsdorff - a casa com o menor numero 
               de vizinhos nao visitados
            7. repetir os passos 4, 5 e 6 ate que visite todas as casas do ta-
               buleiro ou que se chegue em um beco sem saida, ocorrendo tal si-
               tuacao, colher novamente uma casa aleateoria do inviduo temporario
        """
        # gera dicionario com todos movimentos validos
        movimentos_legais = deepcopy(self.movimentos_legais)

        # gera individuo temporario
        individuo_temporario = [i for i in range(1, self.tamanho_individuo + 1)]

        # colhe casa aleatoria em individuo temporario
        c = individuo_temporario.pop(random.randint(0,len(individuo_temporario) - 1))

        # colhe vizinhanca da casa colhida
        if c in movimentos_legais:
            vizinhanca = movimentos_legais.pop(c)

        # adiciona casa a individuo a ser retornado
        individuo = [c]


        # retira a casa de todas as vizinhacas dos movimentos validos
        for k in movimentos_legais:
            if c in movimentos_legais[k]:
                movimentos_legais[k].remove(c)

        # criterio de ordenacao
        sort_criteria = lambda x, y:\
        -1 if len(movimentos_legais[x]) < len(movimentos_legais[y]) else \
        1 if len(movimentos_legais[x]) > len(movimentos_legais[y]) else 0

        # loop para construcao do individuo
        while len(individuo_temporario) > 0:
            if len(vizinhanca) > 0:
                vizinhanca.sort(sort_criteria)
                c = vizinhanca.pop(0)
            else: # Beco sem Saida
                c = individuo_temporario[random.randint(0,len(individuo_temporario) - 1)]

            # remove casa de individuo temporario
            individuo_temporario.remove(c)

            # colhe vizinhanca da casa colhida
            if c in movimentos_legais:
                vizinhanca = movimentos_legais.pop(c)

            # adiciona casa a individuo a ser retornado
            individuo.append(c)


            # retira a casa de todas as vizinhacas dos movimentos validos
            for k in movimentos_legais:
                if c in movimentos_legais[k]:
                    movimentos_legais[k].remove(c)

        return tuple(individuo)

    def __corrigir_descendentes(self):
        """ corrige individuos dos descendentes com genes repetidos """

        # primeiro passo: criar uma lista com as casas repetidas, mostrando
        # cada casa em repeticao
        # segundo passo: criar uma lista de casas inexistentes, mostrando
        # cada casa faltante
        # terceiro passo, iterar sobre as duas listas e sobre o individuo
        # substituindo no individuo uma casa repetida por uma casa inexis-
        # tente

        for i in range(len(self.descendentes)):
            casas_repetidas = []
            casas_inexistentes = []

            d = self.descendentes

            d[i] = list(d[i]) # configura como lista
            for j in range(1,self.tamanho_individuo + 1):
                ocorrencias = d[i].count(j)
                if ocorrencias == 0:
                    casas_inexistentes.append(j)
                elif ocorrencias > 1:
                    while ocorrencias > 1:
                        casas_repetidas.append(j)
                        ocorrencias -= 1
            for j in range(0, len(casas_repetidas)):
                k = casas_repetidas[j]
                l = casas_inexistentes[j]
                d[i][d[i].index(k)] = l
            d[i] = tuple(d[i]) # retorna a tupla

    def iniciar_populacao(self):
        """ 
            O que e considerado como individuo: 
                um vetor de numero de casas em um tabuleiro

            Abordagens utilizadas:
            -totalmente aleatoria
                permutacao aleatoria dum vetor de 1 -> tamanho_individuo
            -aleatoria entre vizinhos disponiveis
                escolhe um numero entre 1 -> tamanho_individuo aleatoriamente
                adiciona-o na lista de visitados
                atualiza o numero para um de seus vizinhos (aleatoriamente) 
                que nao estao na lista de visitados
                quando nao houver vizinhos nao visitados escolhe aleatoriamente
                um outro elemento qualquer para atualizar numero
                repete o processo ate todos os numeros estarem visitados
                retornando essa lista
            -baseada na regra de warnsdorff
                um numero aleatorio entre 1 e tamanho_individuo e escolhido
                e a partir desse numero, se escolhe o proximo elemento do 
                individuo segundo a regra de warnsdorff que diz que deve-se
                ir a casa nao visitada que contenha o menor numero de vizi-
                nhos nao visitados

            Criterio para construcao da populacao: 
                -se o numero e multiplo de 5 gera-se um individuo warnsdorff
                -se o numero e multiplo de 3 (mas nao de 5) gera-se um indivi
                 duo aleatorio 
                -para o restante, gera-se individuos aleatorios entre os vizi
                 nhos disponiveis
                Essa abordagem e adequada para a geracao de uma pop. heteroge-
                nea

        """        
        for i in range(1, self.tamanho_populacao+1):
            e = self.__individuo_warnsdorff() if i % 7 == 0 else \
                self.__individuo_aleatorio() if i % 3 == 0 else \
                self.__individuo_aleatorio_disponiveis() 

            self.populacao.append(e)
        random.shuffle(self.populacao)

    def avaliar_populacao(self):
        """ Metodo que preenche dicionario de fitness para cada individuo """
        for individuo in self.populacao + self.descendentes:
            self.valor_individuos[individuo] = self.fitness(individuo)

    def selecionar_populacao(self):
        """ 
            Metodo que seleciona os individuos de uma populacao
            pelo metodo da roleta
        """
        valor_total = 0
        roleta = {}
        individuos_selecionados = []

        for p in self.populacao:
            valor_total += self.valor_individuos[p]
            roleta[p] = valor_total

        for p in self.populacao:
            giro = random.randint(0, valor_total)
            for q in self.populacao:
                if giro <= roleta[q]:
                    individuos_selecionados.append(q)
                    break

        self.populacao = individuos_selecionados

    def reproduzir_populacao(self):
        """
            Metodo que reproduz a populacao pelo criterio ponto duplo de corte
            heuristico -> que seta a area de corte na maior sequencia valida
        """

        """
            inner function para calcular a area do ponto duplo de corte, cor-
            respondente a maior sequencia valida
            Entrada: individuo
            Saida: inicio_sequencia
                   fim_sequencia
        """
        def calcula_ponto_duplo_de_corte(individuo):
            inicio_sequencia = 0
            fim_sequencia = 0
            aptidao = 0
            aptidao_local = 0

            movimentos_legais = deepcopy(self.movimentos_legais)

            i = 0
            while i < len(individuo) - 1:
                j = i
                while j < len(individuo) - 1 and individuo[j + 1] in movimentos_legais[individuo[j]]:
                    aptidao_local += 1
                    if aptidao < aptidao_local:
                        aptidao = aptidao_local
                        inicio_sequencia, fim_sequencia = i, j
                    j += 1
                i = j + 1
                aptidao_local = 0
            return inicio_sequencia, fim_sequencia
        
        # parea individuos de dois em dois
        pais = []
        maes = []
        for i in range(0,self.tamanho_populacao,2):
            pais.append(self.populacao[i])
            maes.append(self.populacao[i + 1])

        # comeca a gerar os descendentes
        for i in range(0, self.tamanho_populacao/2):
            # determina sequencias de movimentos legais possiveis
            sequencias = [calcula_ponto_duplo_de_corte(pais[i]), \
                          calcula_ponto_duplo_de_corte(maes[i])]

            # pega o inicio e o final da maior sequencia
            inicio_sequencia, fim_sequencia = \
            max(sequencias, key=lambda x: x[1] - x[0])
            
            # primeiro descendente - pai, mae, pai
            descendente_1 = () 
            descendente_1 += tuple(pais[i][0:inicio_sequencia])
            descendente_1 += tuple(maes[i][inicio_sequencia:fim_sequencia])
            descendente_1 += tuple(pais[i][fim_sequencia:])

            # segundo descendente - mae, pai, mae
            descendente_2 = ()
            descendente_2 += tuple(maes[i][0:inicio_sequencia])
            descendente_2 += tuple(pais[i][inicio_sequencia:fim_sequencia])
            descendente_2 += tuple(maes[i][fim_sequencia:])

            self.descendentes.append(descendente_1)
            self.descendentes.append(descendente_2)
        self.__corrigir_descendentes()

    def mutar_populacao(self):
        """
            Operador de mutacao baseado na troca de uma casa com
            outra que possua um vizinho pertencente a seu conjunto
            troca por vizinho valido
        """

        movimentos_legais = deepcopy(self.movimentos_legais)

        for individuo in self.populacao + self.descendentes:
            p = random.random()
            if p < self.probabilidade_mutacao:
                c = random.choice(individuo) # uma casa qualquer do individuo
                for i in range(0, self.tamanho_individuo - 1):
                    # quando alguem possui mesma vizinho de c e nao e c
                    if individuo[i + 1] in movimentos_legais[c] \
                       and individuo[i] is not c:
                        individuo = list(individuo)
                        individuo[i], c = c, individuo[i]
                        individuo = tuple(individuo)


    def renovar_populacao(self):
        """ 
            metodo para renovacao de individuos da populacao segundo criterio
            metade da populacao corrente mais apta e metade dos descendentes
            mais aptos
        """

        sort_criteria = lambda x, y: -1 if self.fitness(x) < self.fitness(y)\
                                     else 1 if self.fitness(x) > self.fitness(y)\
                                     else 0

        self.populacao.sort(sort_criteria, reverse=True)
        self.descendentes.sort(sort_criteria, reverse=True)

        self.populacao = self.populacao[0:self.tamanho_populacao/2] + self.descendentes[0:self.tamanho_populacao/2]
        self.descendentes = []
        self.populacao.sort(sort_criteria, reverse=True)

    def executar(self):
        """ para executar o AG """
    
        self.iniciar_populacao()
        self.avaliar_populacao()
        Otimo = False

        for g in range(self.geracoes):
            self.selecionar_populacao()
            self.reproduzir_populacao()
            self.mutar_populacao()
            self.avaliar_populacao()
            self.renovar_populacao()
            # teste de condicao para estao Otimo
            if self.fitness(self.populacao[0]) == (self.tamanho_individuo - 1):
                Otimo = True
                break

        return self.populacao[0], Otimo
