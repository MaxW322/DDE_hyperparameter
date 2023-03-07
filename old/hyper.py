import matlab.engine
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from hyperopt import Trials
from hyperopt import fmin
from hyperopt import hp
from hyperopt import tpe

eng = matlab.engine.start_matlab()
tf = eng.isprime(37)

# 参数设置
fspace = {
    'i_I': hp.uniform('i_I', 0, 1),
    'i_Q': hp.uniform('i_Q', 0, 1),
    'beta_iq': hp.uniform('beta_iq', 0, 1),
    'beta_ir': hp.uniform('beta_ir', 0, 1),
    'beta_qr': hp.uniform('beta_qr', 0, 1),
    'gamma_2': hp.uniform('gamma_2', 0, 1),
    'beta_bd': hp.uniform('beta_bd', 0, 1)
}


# 求解函数：参数传入matlab，返回同真实值的误差
def func(para):
    i_I = para['i_I']
    i_Q = para['i_Q']
    beta_iq = para['beta_iq']
    beta_ir = para['beta_ir']
    beta_qr = para['beta_qr']
    gamma_2 = para['gamma_2']
    beta_bd = para['beta_bd']
    params_input = (i_I, i_Q, beta_iq, beta_ir, beta_qr, gamma_2, beta_bd)
    error = eng.para(params_input)

    return error

trials = Trials()
best = fmin(fn=func, space=fspace, algo=tpe.suggest, max_evals=10, trials=trials)

print('best:', best)
print('trials:')
# for trial in trials.trials[:-1]:
#     print(trial)
print(trials.trials[-1])

# parameters = ['i_I', 'i_Q', 'beta_iq', 'beta_ir', 'beta_qr', 'gamma_2', 'beta_bd']

p = best


def huatu(p):
    i_I = p['i_I']
    i_Q = p['i_Q']
    beta_iq = p['beta_iq']
    beta_ir = p['beta_ir']
    beta_qr = p['beta_qr']
    gamma_2 = p['gamma_2']
    beta_bd = p['beta_bd']
    params = (i_I, i_Q, beta_iq, beta_ir, beta_qr, gamma_2, beta_bd)
    sols = eng.fit_output(params)
    return sols


for var in p:
    p[f'{var}'] = float(p[f'{var}'])

sol = huatu(p)
y4 = list(sol[0])
t = np.linspace(1, len(y4), len(y4))
l4 = plt.plot(t, y4)

data0 = pd.read_csv('../data/currentconfirmed.csv', header=None)
data0 = pd.DataFrame(data0.values.T, index=data0.columns, columns=data0.index)
data = data0.values.tolist()
data1 = data[0][0:135]
actual = plt.plot(t, data1)

plt.grid(linestyle='-.', alpha=0.2)
plt.xlabel('day')
plt.ylabel('number')
# plt.ylim(0, 800)
plt.xlim(0, 135)
bl = best
plt.legend(["Q", "actual"], loc='upper right')
plt.show()

i = 1
if i == 1:
    print(i)