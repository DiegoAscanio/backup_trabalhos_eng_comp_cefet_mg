import scipy.signal
import numpy as np
from matplotlib import pyplot
import pdb

step = lambda k: 1**k
ramp = lambda k: k
par = lambda k: k**2
sin = lambda k: np.sin(k)
K = 0.5
T = 0.1

A = np.array([[0, 1], [-K, 0]])
Az = T*A + np.identity(2)
B = np.array([[0],[1]])
Bz = T*B
C = np.array([K, 0])
D = np.array([0])

time = np.linspace (0, 100, 1001)
U = {}
#U['u_step'] = np.array([step(t) for t in time])
#U['u_ramp'] = np.array([ramp(t) for t in time])
#U['u_par'] = np.array([par(t) for t in time])
U['u_sin'] = np.array([sin(t) for t in time])

subplots = {}

for u in U:
    time_t, y_t, x_t = scipy.signal.lsim((A,B,C,D), U[u], time)
    time_k, y_k, x_k = scipy.signal.dlsim((Az,Bz,C,D,T), U[u], time)
    y_k = y_k[:,0]

    pyplot.plot(time,U[u],'-',label=u)
    pyplot.plot(time_k,y_k,':',label='Y_k_'+u)
    pyplot.plot(time_t,y_t,',',label='Y_t_'+u)


pyplot.legend()
pyplot.show()
