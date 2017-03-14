#!/usr/bin/python3
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

# reduzindo o conjunto de pontos

v_l['x'] = v_l['x'][v_l['y'].index(-0.24):]
v_l['y'] = v_l['y'][v_l['y'].index(-0.24):]

# adicionando diferenças necessarias para iniciar em 0,0
v_l['x'] = [v_l['x'][i] + 1.05e-06 for i in range(0, len(v_l['x']))]
v_l['y'] = [v_l['y'][i] + 0.24 for i in range(0, len(v_l['y']))]

v_l['y'] = [v_l['y'][i] for i in range (0, len(v_l['y']), 10)]
v_l['x'] = [v_l['x'][i] for i in range (0, len(v_l['x']), 10)]

# plotting dos gráficos
pyplot.plot(v_l['x'], v_l['y'], 'o')
pyplot.show()
