#!/usr/bin/python
import sys
import csv
import numpy
import scipy.signal
from matplotlib import pyplot

# funcao de transferencia em malha aberta
gma = lambda K = 0.02525, tau = 100 : scipy.signal.TransferFunction([K], [tau, 1])

# saida do osciloscopio
time_Y = []
Y = []

# canal 1
with open('F0000CH1.CSV', newline='\n') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for row in spamreader:
        time_Y.append(float(row[3]))
        Y.append(float(row[4]))

# entrada simulada
time_U = [t for t in time_Y]
U = [0 if t < 40 else 12 for t in time_U]
#U = [12 for t in time_U]

# simulacao
y_0 = 0.297
time_sim, y_sim, states = scipy.signal.lsim(gma(), U, time_U)

# plot
pyplot.plot(time_Y, Y, ':')
pyplot.plot(time_sim, y_sim+y_0, '-')
pyplot.show()
