import scipy.signal
import numpy as np
from matplotlib import pyplot
import pdb

step = lambda k: 1**k
ramp = lambda k: k
par = lambda k: k**2
sin = lambda k: np.sin(k)
R = 220
L = 220*10**-6
C = 1*10**-9
T = 0.000001

A = np.array([[0, 1], [-1/(L*C), -R/L]])
Az = T*A + np.identity(2)
B = np.array([[0],[1]])
Bz = T*B
C = np.array([1/(L*C), 0])
D = np.array([0])

time = np.linspace (0, 0.00002, 601)
U = {}
#U['u_step'] = np.array([step(t) for t in time])
#U['u_ramp'] = np.array([ramp(t) for t in time])
#U['u_par'] = np.array([par(t) for t in time])
#U['u_sin'] = np.array([sin(t) for t in time])

#Entrada V_s V
V_s = 2
U['u_step'] = np.array([V_s*step(t) for t in time])

subplots = {}

for u in U:
    time_t, y_t, x_t = scipy.signal.lsim((A,B,C,D), U[u], time)
    #time_k, y_k, x_k = scipy.signal.dlsim((Az,Bz,C,D,T), U[u], time)
    #y_k = y_k[:,0]

    pyplot.plot(time,U[u],'-',label=u)
    #pyplot.plot(time_k,y_k,':',label='Y_k_'+u)
    pyplot.plot(time_t,y_t,',',label='Y_t_'+u)


pyplot.legend()
pyplot.show()
