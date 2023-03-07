import matlab.engine
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time
from datetime import datetime
from time import strftime, gmtime
from hyperopt import STATUS_OK
from hyperopt import Trials
from hyperopt import fmin
from hyperopt import hp
from hyperopt import tpe
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from math import sqrt
from para2data import para2data
import sys

# 调用matlab
eng = matlab.engine.start_matlab()
tf = eng.isprime(37)

# 参数设置
fspace_all = {
    'i_I': hp.uniform('i_I', 0, 1),
    'i_Q': hp.uniform('i_Q', 0, 1),
    'beta_iq': hp.uniform('beta_iq', 0, 1),
    'beta_ir': hp.uniform('beta_ir', 0, 1),
    'beta_qr': hp.uniform('beta_qr', 0, 1),
    'gamma_2': hp.uniform('gamma_2', 0, 1),
    'beta_bd': hp.uniform('beta_bd', 0, 1)
}

fspace = {
    'i_I': hp.uniform('i_I', 0, 1),
    'i_Q': hp.uniform('i_Q', 0, 1)
}


# 求解函数：参数传入matlab，返回同真实值的误差
def fit_output(p):
    i_I = p['i_I']
    i_Q = p['i_Q']
    beta_iq = p['beta_iq']
    beta_ir = p['beta_ir']
    beta_qr = p['beta_qr']
    gamma_2 = p['gamma_2']
    beta_bd = p['beta_bd']
    params = (i_I, i_Q, beta_iq, beta_ir, beta_qr, gamma_2, beta_bd)
    sols = eng.fit_output_all(params)
    return sols


def hyper_para(para_c, pos):
    def func(para):
        i_I = para['i_I']
        i_Q = para['i_Q']
        beta_iq = para_c['beta_iq']
        beta_ir = para_c['beta_ir']
        beta_qr = para_c['beta_qr']
        gamma_2 = para_c['gamma_2']
        beta_bd = para_c['beta_bd']
        params_input = (i_I, i_Q, beta_iq, beta_ir, beta_qr, gamma_2, beta_bd, float(pos))
        error = eng.para_all_divide_2para(params_input)
        return error

    trials = Trials()
    best = fmin(fn=func, space=fspace, algo=tpe.suggest, max_evals=7500, max_queue_len=10, trials=trials)

    print('best:', best)

    # 将得出的best参数传入fit_output函数，输出该参数下的数据
    p = {}
    for var in best:
        p[f'{var}'] = float(best[f'{var}'])
    for var in ['beta_iq', 'beta_ir', 'beta_qr', 'gamma_2', 'beta_bd']:
        p[f'{var}'] = float(para_c[f'{var}'])
    sols = fit_output(p)
    sols = [[row[i] for row in sols] for i in range(len(sols[0]))]
    y = pd.DataFrame(data=sols, columns=['S', 'E', 'I', 'Q', 'R', 'N'])
    return p, y.iloc[pos - 1, :]


def hyper_const():
    def func1(para):
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

    best = fmin(fn=func1, space=fspace_all, algo=tpe.suggest, max_evals=10000, max_queue_len=10)
    p = {}
    for var in best:
        p[f'{var}'] = float(best[f'{var}'])
    return p


# 调试：导出拟合图像与数据
if __name__ == '__main__':
    fit_data = pd.DataFrame(columns=['S', 'E', 'I', 'Q', 'R', 'N'])
    best_para = pd.DataFrame()
    actual_data = pd.read_csv('./data/currentconfirmed.csv', header=None)
    column_para = []

    para_const = hyper_const()

    bp = 1
    tic = time.perf_counter()

    plt.figure(1)
    # 135逐点遍历
    print(f"\n")
    for i in range(135):
        ttc = time.perf_counter()
        # print(f"\033[1;34m current time: {ttc-tic:0.4f}s \033[0m position -> \033[1;31m {i + 1} \033[0m")
        print("\033[1;34m current time: ", strftime("%H:%M:%S", gmtime(ttc - tic)),
              f"\033[0m position (day) -> \033[1;31m {i + 1} \033[0m")
        best_p, y = hyper_para(para_const, i + 1)
        fit_data = pd.concat((fit_data, pd.DataFrame(y).T), axis=0)
        fit_data = fit_data.reset_index().drop(columns='index')
        # 实时拟合图
        plt.clf()
        tp_p = pd.DataFrame(pd.concat((fit_data['Q'], actual_data.iloc[0:i + 1]), axis=1))
        plt.plot(tp_p)
        plt.title(f'pos = {i + 1}')
        plt.legend(['fit', 'real'])
        plt.pause(0.1)

        # 存一次参数名称至列名
        if bp:
            for var in best_p:
                column_para.append(var)
            bp = 0

        temp = []
        for var in best_p:
            temp.append(best_p[var])
        best_para = pd.concat((best_para, pd.DataFrame(temp).T), axis=0)

    # 总计算时间
    toc = time.perf_counter()
    print('/r', end='')
    print("\033[1;34m finished time: ", strftime("%H:%M:%S", gmtime(toc - tic)), "\033[0m", end='')
    sys.stdout.flush()
    # 输出文件时间戳
    now_time = datetime.now()
    now = now_time.strftime("%Y-%m-%d %H.%M.%S")
    # 输出135个点的最优参数
    best_para.columns = column_para
    # print(best_para)
    best_para.reset_index()
    best_para.to_csv(f'./output/paras/best_para_all {now}.csv', index=False)
    print('output parameters')

    # 输出135x6个点拟合值
    fit = pd.DataFrame()
    fit['fit_data'] = fit_data['Q']
    fit_data.to_csv(f'./output/fit_data/fit_all_five {now}.csv', index_label=None)
    print('output fit data')

    # 输出拟合rmse
    f = open('./output/rmse.txt', 'a')
    fit['real_data'] = pd.read_csv('./data/currentconfirmed.csv', header=None)
    rmse = sqrt(mean_squared_error(fit['fit_data'], fit['real_data']))
    f.write(f'rmse-{now} = {rmse}\n')
    r2 = r2_score(fit['fit_data'], fit['real_data'])
    f.write(f'r2-{now} = {r2}\n')
    f.close()
    print('output rmse,r2')

    # 最后总绘制拟合情况图
    print('plot fit')
    plt.figure(2)
    plt.plot(fit)
    plt.legend(['fit', 'real'])
    plt.title(f'rmse-{now} = {rmse}\n')
    plt.savefig(f'./output/fig/all_data {now}.png')
    plt.show()
    print('ALL END')
    # # 输出最优参数(ban)
    # f = open('./output/para_all.txt','a')
    # print(best_para,file=f)
    # f.close()
    plt.figure()
    plt.plot(fit_data)
    plt.legend(fit_data.columns)
    plt.show()