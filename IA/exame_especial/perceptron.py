import random
import copy
def train_perceptron(X, Y, n=0.25, iter_max=1000000): # n taxa de aprendizado
    w = [random.random() - 0.5 for c in range(len(X[0])+1)]
    X_n = X
    X_n.insert(0,[1 for c in range(len(X[0]))]) # insercao do bias
    e = 0 # erro esperado
    k = 0 # numero de iteracoes
    while e != 1 and k < iter_max: # enquanto nao se alcanca os valores esperados
        e = 1
        indexes = [j for j in range(len(X_n[0]))]
        random.shuffle(indexes)
        for j in indexes:
            # calculo da rede
            net = 0
            for i in range(len(X_n)):
                net = net + w[i]*X_n[i][j]
            y = 1 if net > 0 else 0
            error = Y[j] - y
            if error != 0:
                e = 0
                for i in range(len(X_n)):
                    w[i] = w[i] + n*error*X_n[i][j]
        k += 1
    # apos treinamento, averiguacao de funcionamento
    y_obtido = []
    for j in range(len(X_n[0])):
        net = 0
        for i in range(len(X_n)):
            net = net + w[i]*X_n[i][j]
        y = 1 if net > 0 else 0
        y_obtido.append(y)
    return k, w, y_obtido

# Y e 1 para quando todos os elementos da coluna de X forem > 0
# e 0 caso contrario
X = [[0, 0, 0],
     [1, 0, 0],
     [0, 1, 0]]
Y = [0, 1, 0]
print(train_perceptron(X,Y))
