#!/usr/bin/python
import sys
import csv
import numpy
import scipy.signal
from matplotlib import pyplot

if len(sys.argv) != 2:
    print('Uso: ./simulacao.py <Kp>')
    sys.exit(0)

# funcao de transferencia em malha fechada
hmf = lambda Kp, R=1*10**5, C=2*10**-7: scipy.signal.TransferFunction([Kp], [R*C, (1+Kp)])
Kp = int(sys.argv[1])

# entrada do osciloscopio
time_U = []
U = []

# saida do osciloscopio
time_Y = []
Y = []

# canal 1
with open(str(Kp)+'/CH1.CSV', newline='\n') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for row in spamreader:
        time_U.append(float(row[3]))
        U.append(float(row[4]))

# canal 2
with open(str(Kp)+'/CH2.CSV', newline='\n') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for row in spamreader:
        time_Y.append(float(row[3]))
        Y.append(float(row[4]))

# simulacao

time_sim, y_sim, states = scipy.signal.lsim(hmf(Kp), U[time_U.index(0):], time_U[time_U.index(0):])

# plot
pyplot.plot(time_U, U, ':')
pyplot.plot(time_Y, Y, ':')
pyplot.plot(time_sim, y_sim, '-')
pyplot.show()
