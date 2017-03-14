from genetico import AlgoritmoGeneticoPasseioCavalo
import pdb
import sys
import numpy
import time

print('n,min,max,media,desvio_padrao,tempo')

for n in [5, 8, 16]:
    valores = []
    inicio = time.time()

    for i in range(30):
        ag_ppc = AlgoritmoGeneticoPasseioCavalo (n, 100, 10, 0.25)
        individuo, otimo = ag_ppc.executar()
        valores.append(ag_ppc.fitness(individuo))

    media = round(numpy.mean(valores), 4)
    desvio_padrao = round(numpy.sqrt(numpy.var(valores)), 4)
    fim = round(time.time() - inicio, 2)

    print(str(n)+','+str(min(valores))+','+str(max(valores))+','+\
      str(media)+','+str(desvio_padrao)+','+str(fim))
