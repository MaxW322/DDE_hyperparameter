import matlab.engine
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from hyperopt import STATUS_OK
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


start_num = [1, 28, 55, 82, 109]
endin_num = [27, 54, 81, 108, 135]


def fit_output(p):
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


def hyper_para(start, endin):
    def func(para):
        i_I = para['i_I']
        i_Q = para['i_Q']
        beta_iq = para['beta_iq']
        beta_ir = para['beta_ir']
        beta_qr = para['beta_qr']
        gamma_2 = para['gamma_2']
        beta_bd = para['beta_bd']
        params_input = (i_I, i_Q, beta_iq, beta_ir, beta_qr, gamma_2, beta_bd, float(start), float(endin))
        error = eng.para_divide(params_input)
        return error

    trials = Trials()
    best = fmin(fn=func, space=fspace, algo=tpe.suggest, max_evals=10000, trials=trials)
    print('best:', best)
    p = best
    for var in p:
        p[f'{var}'] = float(p[f'{var}'])
    sol = fit_output(p)
    y4 = list(sol[0])

    return best, y4[start:endin]


# test
# if __name__ == '__main__':
#     best_para = {}
#     fit_data = []
#     for i in range(len(start_num)):
#         [best_p, y] = hyper_para(start=start_num[i], endin=endin_num[i])
#         best_para[f'best_{i + 1}'] = best_p
#         fit_data.extend(y)

if __name__ == '__main__':
    best_para = {}
    fit_data = []
    for i in range(len(start_num)):
        best_p, y = hyper_para(start=start_num[i], endin=endin_num[i])
        best_para[f'best_{i + 1}'] = best_p
        fit_data.extend(y)

    print(best_para)
    fit = pd.DataFrame()
    fit['fit_data'] = fit_data
    fit['real_data'] = pd.read_csv('../data/currentconfirmed.csv')
    fit.to_csv('./output/output_five.csv')
    plt.figure()
    plt.plot(fit)
    plt.legend(['fit', 'real'])
    plt.savefig('./output/5_data.png')
    plt.show()
    f = open('../output/para_five.txt', 'a')
    print(best_para,file=f)
    f.close()

# t = np.linspace(1, len(y4), len(y4))
# l4 = plt.plot(t, y4)
#
# data0 = pd.read_csv('data/currentconfirmed.csv', header=None)
# data0 = pd.DataFrame(data0.values.T, index=data0.columns, columns=data0.index)
# data = data0.values.tolist()
# data1 = data[0][0:135]
# actual = plt.plot(t, data1)
#
# plt.grid(linestyle='-.', alpha=0.2)
# plt.xlabel('day')
# plt.ylabel('number')
# # plt.ylim(0, 800)
# plt.xlim(0, 135)
# bl = best
# plt.legend(["Q", "actual"], loc='upper right')
# plt.show()

# 5 divide fit result
# best1 = {'beta_bd': 0.23347785687055228, 'beta_iq': 0.0016729189765935276, 'beta_ir': 0.41728939742929894,
#          'beta_qr': 0.642945984947796, 'gamma_2': 0.9968907075245604, 'i_I': 0.07411699068747907,
#          'i_Q': 0.8561534120633854}
# best2 = {'beta_bd': 0.6634428962843361, 'beta_iq': 0.0016019041706399786, 'beta_ir': 0.5891266531180747,
#          'beta_qr': 0.8901974053792958, 'gamma_2': 0.7372233153366033, 'i_I': 0.13065550702022888,
#          'i_Q': 0.990217420375974}
# best3 = {'beta_bd': 0.17938423140887863, 'beta_iq': 0.0007218858316697646, 'beta_ir': 0.21935919681565705,
#          'beta_qr': 0.9998782620619476, 'gamma_2': 0.9826403412317257, 'i_I': 0.725270712692139,
#          'i_Q': 0.6684387718908166}
# best4 = {'beta_bd': 0.590936487425906, 'beta_iq': 0.0016620794170064993, 'beta_ir': 0.732662810915278,
#          'beta_qr': 0.9982273424871208, 'gamma_2': 0.37950472488138065, 'i_I': 0.10947309528216426,
#          'i_Q': 0.892764393631747}
# best5 = {'beta_bd': 0.4747401781197773, 'beta_iq': 0.002498224378128966, 'beta_ir': 0.8858634791169262,
#          'beta_qr': 0.7296461285717761, 'gamma_2': 0.9401624090721328, 'i_I': 0.08813672878894596,
#          'i_Q': 0.9992037201719626}

# vall = locals()
#
# final = []
#
# fit_data = pd.DataFrame()
# for i in range(5):
#     fit = fit_output(vall[f'best{i + 1}'])
#     y4 = list(fit[0])
#     final.extend(y4[start_num[i]:endin_num[i]])
#
# fit_data['fit'] = final
# fit_data['real_data'] = pd.read_csv('./data/currentconfirmed.csv')
#
# plt.figure()
# plt.plot(fit_data)
# plt.legend(['fit', 'real'])
#
# plt.savefig('./output/5_data.png')
# plt.show()
