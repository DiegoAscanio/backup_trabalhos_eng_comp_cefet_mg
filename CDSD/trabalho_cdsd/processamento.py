from scipy.optimize import curve_fit
from scipy.signal import TransferFunction
from matplotlib import pyplot

import csv
import numpy

#v_s = {} # tensão da entrada
#v_s['x'] = []
#v_s['y'] = []

v_c = {} # tensão da saída - indutor
v_c['x'] = []
v_c['y'] = []


# leitura dos dados do canal 1 - entrada degrau
#with open('ch1_tratado.csv', newline='\n') as csvfile:
#    spamreader = csv.reader(csvfile, delimiter = ',')
#    for row in spamreader:
#        v_s['x'].append(row[3])
#        v_s['y'].append(row[4])

# leitura dos dados do canal 2 - saída do indutor
with open('F0001CH2.CSV', newline='\n') as csvfile:
    spamreader = csv.reader(csvfile, delimiter = ',')
    for row in spamreader:
        v_c['x'].append(row[3])
        v_c['y'].append(row[4])

# convertendo os dados para valores numéricos

v_c['x'] = [float(x) for x in v_c['x']]
v_c['y'] = [float(y) for y in v_c['y']]

''' resposta do indutor a entrada degrau:
    V_l = V_s*e^(-t*(R/L))
'''
f = lambda t, V, R, C: V * (1 - numpy.exp(-t/(R*C)))

# fiting dos parametros da curva para t >= 0
popt, pcov = curve_fit(f, v_c['x'][v_c['x'].index(0.):], v_c['y'][v_c['x'].index(0.):])

v_c_adj = [ f(x, popt[0], popt[1], popt[2]) for x in v_c['x'][v_c['x'].index(0.):]]

# impressão dos parametros da curva:
print(popt)

# impressão do erro / desvio padrão
print(numpy.sqrt(numpy.diag(pcov)))

# plotting dos gráficos - a ser melhorado:
pyplot.plot(v_c['x'][v_c['x'].index(0.):],v_c['y'][v_c['x'].index(0.):],'x',v_c['x'][v_c['x'].index(0.):],v_c_adj,'r-')
pyplot.show()
