from matplotlib import pyplot
import numpy

# funcoes

''' H(s) = G(s)/(1 + G(s)); L^-1[H(s)] = k^(0.5)*sin(k^(0.5)*t)
'''

#H = lambda t, k: numpy.sqrt(k)*numpy.sin(numpy.sqrt(k)*t)
H = lambda t, k: k*t

''' R1(t) = k*t^2; L[R1(t)] = k/s^3
'''

R1 = lambda t, k: k*t**2

''' R2(t) = t^2 -12*t + 36; L[R2(t)] = (36*s^2 -12*s + 2) / s^3
'''

R2 = lambda t: t**2 - 12*t + 36

''' R3 = R1 + R2
'''

R3 = lambda t, k: k*t**2 + t**2 - 12*t + 36

''' definindo o intervalo de tempo
'''

time = numpy.linspace(0,10000,21)

U1 = [R1(t, 1) for t in time]
U2 = [R2(t) for t in time]
U3 = [R3(t, 1) for t in time]

Y1 = [R1(t, 0.5)*H(t, 0.5) for t in time]
Y2 = [R2(t)*H(t, 1) for t in time]
Y3 = [R3(t, 0.5)*H(t, 0.5) for t in time]

''' plot das entradas '''
pyplot.plot(time, U1, 'ko', time, U2, 'bo', time, U3, 'ro')
''' plot dos sinais '''
#pyplot.plot(time, U1, 'ko', time, U2, 'bo', time, U3, 'ro', time, Y1, 'kx', time, Y2, 'bx', time, Y3, 'rx')
''' plot das saidas '''
#pyplot.plot(time, Y1, 'kx', time, Y2, 'bx', time, Y3, 'rx')

pyplot.show()
