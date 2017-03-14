import scipy.signal
import numpy as np
from matplotlib import pyplot
import pdb

step = lambda k: 1**k
ramp = lambda k: k
sin = lambda k: np.sin(k)

'''
K = 0.5
T = 0.1
'''

time = np.linspace (0, 100, 1001)
U = {}
U['u_step'] = np.array([step(t) for t in time])
U['u_ramp'] = np.array([ramp(t) for t in time])
U['u_sin'] = np.array([sin(t) for t in time])

'''
    Continuous Transfer Function:
    0.5 / (s^2 + 0.5)
'''
continuous_num = [0., 0., 0.5]
continuous_den = [1., 0., 0.5]

'''
    Discrete Transfer Function:
    (0.0025z + 0.0025) / (z^2 - 1.995z + 1)
'''
discrete_num = [0., 0.0025, 0.0025]
discrete_den = [1., -1.995, 1.]

for u in U:
    time_t, y_t, x_t = scipy.signal.lsim((continuous_num,continuous_den), U[u], time)
    time_k, y_k = scipy.signal.dlsim((discrete_num, discrete_den, 0.1), U[u], time)
    y_k = y_k[:,0]

    pyplot.plot(time,U[u],'-',label=u)
    pyplot.plot(time_k,y_k,',',label='Y_k_'+u)
    pyplot.plot(time_t,y_t,',',label='Y_t_'+u)


pyplot.legend()
pyplot.show()
