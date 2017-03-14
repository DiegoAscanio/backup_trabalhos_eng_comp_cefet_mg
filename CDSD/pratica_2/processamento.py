from scipy.optimize import curve_fit
from scipy.signal import TransferFunction
from matplotlib import pyplot

import csv
import numpy

v_s = {} # tensão da entrada
v_s['x'] = []
v_s['y'] = []

v_l = {} # tensão da saída - indutor
v_l['x'] = []
v_l['y'] = []


# leitura dos dados do canal 1 - entrada degrau
with open('ch1_tratado.csv', newline='\n') as csvfile:
    spamreader = csv.reader(csvfile, delimiter = ',')
    for row in spamreader:
        v_s['x'].append(row[0])
        v_s['y'].append(row[1])

# leitura dos dados do canal 2 - saída do indutor
with open('ch2_tratado.csv', newline='\n') as csvfile:
    spamreader = csv.reader(csvfile, delimiter = ',')
    for row in spamreader:
        v_l['x'].append(row[0])
        v_l['y'].append(row[1])

# convertendo os dados para valores numéricos

v_l['x'] = [float(x) for x in v_l['x']]
v_l['y'] = [float(y) for y in v_l['y']]

''' resposta do indutor a entrada degrau:
    V_l = V_s*e^(-t*(R/L))
'''
f = lambda t, V, R, L: V * numpy.exp(-t*(R/L))

# fiting dos parametros da curva para t >= 0
popt, pcov = curve_fit(f, v_l['x'][v_l['x'].index(0.):], v_l['y'][v_l['x'].index(0.):])

# impressão dos parametros da curva:
print(popt)

# impressão do erro / desvio padrão
print(numpy.sqrt(numpy.diag(pcov)))

# plotting dos gráficos - a ser melhorado:
#pyplot.plot(v_l['x'],v_l['y'],'o')
#pyplot.show()
