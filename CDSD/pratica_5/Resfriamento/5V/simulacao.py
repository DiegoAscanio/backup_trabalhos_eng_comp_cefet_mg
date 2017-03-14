#!/usr/bin/python
import sys
import csv
import numpy
import scipy.signal
from matplotlib import pyplot

# funcao de transferencia em malha aberta
gma = lambda b, tau, delta: scipy.signal.TransferFunction([(b + delta*numpy.exp(tau)), (tau*b)], [1, tau])

f = lambda b, tau, delta, t: delta*numpy.exp(-tau*t) + b

# saida do osciloscopio
time_Y = []
Y = []

# canal 1
with open('F0000CH1.CSV', newline='\n') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for row in spamreader:
        time_Y.append(float(row[3]))
        Y.append(float(row[4]))

Y = Y[time_Y.index(50.):]
time_Y = [t - 50. for t in time_Y[time_Y.index(50.):]]
print(len(time_Y),len(Y))

# entrada simulada
time_U = [t for t in time_Y]
#U = [0 if t < 70 else 1 for t in time_U]
U = [1 for t in time_U]

# simulacao
#y_0 = 0.297
print(gma(0.33, 0.04, 0.29))
time_sim, y_ma_sim, states = scipy.signal.lsim(gma(0.33, 0.04, 0.29), U, time_U)
y_sim = [f(0.33, 0.04, 0.29, t) for t in time_Y]

# plot
pyplot.plot(time_Y, Y, ':')
pyplot.plot(time_sim, y_ma_sim, ':')
pyplot.plot(time_Y, y_sim, ':')
pyplot.show()
