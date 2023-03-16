import matlab.engine
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time
from datetime import datetime
from time import strftime, gmtime
import sys
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from math import sqrt

# 调用matlab
print('\n 正在拉起MATLAB ヾ(•ω•`)o')
eng = matlab.engine.start_matlab()
tf = eng.isprime(37)
print('拉起MATLAB成功 ╰(*°▽°*)╯')


# TODO 实现读取参数，返回数据，计算时间

# 定参数输入，基础模型输出
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
    sols = [[row[i] for row in sols] for i in range(len(sols[0]))]
    y = pd.DataFrame(data=sols, columns=['S', 'E', 'I', 'Q', 'R', 'N'])
    fit_data = y
    fit_data = fit_data.reset_index().drop(columns='index')
    return fit_data

# 时变参数输入，基础模型导出
def para2data_all(file_name):
    tic = time.perf_counter()
    para = pd.read_csv(f'./output/paras/{file_name}', index_col=None)
    fit_data = pd.DataFrame(columns=['S', 'E', 'I', 'Q', 'R', 'N'])
    for i in range(len(para)):
        i_I = float(para['i_I'][i])
        i_Q = float(para['i_Q'][i])
        beta_iq = float(para['beta_iq'][i])
        beta_ir = float(para['beta_ir'][i])
        beta_qr = float(para['beta_qr'][i])
        gamma_2 = float(para['gamma_2'][i])
        beta_bd = float(para['beta_bd'][i])
        params = (i_I, i_Q, beta_iq, beta_ir, beta_qr, gamma_2, beta_bd)
        sols = eng.fit_output_all(params)
        sols = [[row[i] for row in sols] for i in range(len(sols[0]))]
        y = pd.DataFrame(data=sols, columns=['S', 'E', 'I', 'Q', 'R', 'N'])
        y_line = y.iloc[i, :]
        fit_data = pd.concat((fit_data, pd.DataFrame(y_line).T), axis=0)
        fit_data = fit_data.reset_index().drop(columns='index')
        print("\r", end="")
        print(i + 1, f'({i})', end="")
        sys.stdout.flush()
    toc = time.perf_counter()
    print("\n\033[1;34m paras to data finished (time): ", strftime("%H:%M:%S", gmtime(toc - tic)), "\033[0m")

    return fit_data

# 时变参数输入，控制模型参数u1, u2, u3
def para2data_all_newmodel(file_name=None, para=pd.DataFrame(), u1=0, u2=0, u3=0):
    tic = time.perf_counter()
    if file_name is not None:
        para = pd.read_csv(f'{file_name}', index_col=None)
    fit_data = pd.DataFrame(columns=['S', 'E', 'I', 'Q', 'R', 'N', 'V'])
    for i in range(len(para)):
        i_I = float(para['i_I'][i])
        i_Q = float(para['i_Q'][i])
        beta_iq = float(para['beta_iq'][i])
        beta_ir = float(para['beta_ir'][i])
        beta_qr = float(para['beta_qr'][i])
        gamma_2 = float(para['gamma_2'][i])
        beta_bd = float(para['beta_bd'][i])
        params = (i_I, i_Q, beta_iq, beta_ir, beta_qr, gamma_2, beta_bd, float(u1), float(u2), float(u3))
        sols = eng.fit_output_all_new_model(params)
        sols = [[row[i] for row in sols] for i in range(len(sols[0]))]
        y = pd.DataFrame(data=sols, columns=['S', 'E', 'I', 'Q', 'R', 'N', 'V'])
        y_line = y.iloc[i, :]
        fit_data = pd.concat((fit_data, pd.DataFrame(y_line).T), axis=0)
        fit_data = fit_data.reset_index().drop(columns='index')
        print("\r", end="")
        print('目前时变参数计算至天数: ', i + 1, f'(索引值: {i})', end="")
        sys.stdout.flush()
    toc = time.perf_counter()
    print("\n\033[1;34m paras to data finished (time): ", strftime("%H:%M:%S", gmtime(toc - tic)), "\033[0m")

    return fit_data

# 废弃了ಥ_ಥ
def para2data(file_name):
    tic = time.perf_counter()
    para = pd.read_csv(f'./output/paras/{file_name}', index_col=None)
    fit_data = pd.DataFrame(columns=['S', 'E', 'I', 'Q', 'R', 'N'])

    i_I = float(para['i_I'][0])
    i_Q = float(para['i_Q'][0])
    beta_iq = float(para['beta_iq'][0])
    beta_ir = float(para['beta_ir'][0])
    beta_qr = float(para['beta_qr'][0])
    gamma_2 = float(para['gamma_2'][0])
    beta_bd = float(para['beta_bd'][0])
    params = (i_I, i_Q, beta_iq, beta_ir, beta_qr, gamma_2, beta_bd)
    sols = eng.fit_output_all(params)
    sols = [[row[i] for row in sols] for i in range(len(sols[0]))]
    y = pd.DataFrame(data=sols, columns=['S', 'E', 'I', 'Q', 'R', 'N'])
    fit_data = y
    fit_data = fit_data.reset_index().drop(columns='index')
    sys.stdout.flush()
    toc = time.perf_counter()
    print("\n\033[1;34m paras to data finished (time): ", strftime("%H:%M:%S", gmtime(toc - tic)), "\033[0m")

    return fit_data

# stri = 'best_para_all test 2023-02-09 20.33.30.csv'
# fit = para2data(stri)
#
# plt.plot(fit)
# plt.show()
