import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np
import pandas as pd
import os
from datetime import datetime
from __para2data import para2data_all_newmodel

# TODO: 输入Dataframe，输出每种人群的变化图
# TODO: 输入Dataframe，输出每种人群与基础模型拟合的比较图
# TODO: 锁定人群排序: ['S', 'E', 'I', 'Q', 'R', 'N', 'V']

text = ['Susceptible Population (S)', 'Exposed Population (E)', 'Infected Population (I)', 'Confirmed Population (Q)',
        'Recovered Population (R)', 'Total Population (N)', 'Vaccinated Population (V)']
pop_column = ['S', 'E', 'I', 'Q', 'R', 'N', 'V']
base_column = ['S', 'E', 'I', 'Q', 'R', 'N']
# colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
colors = ['#1f77b4', '#cc650b', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
# 更暗的屎黄 colors[1]

now_time = datetime.now()
now = now_time.strftime("%Y-%m-%d %H.%M.%S")


# 输出每种人群的变化图
def plot_population(data, population_code=None, save_mode=True):
    global pop_column, now, colors
    if population_code is None:
        for var in enumerate(pop_column):
            # print(var)
            # plt.figure(figsize=(4, 4))
            plt.plot(data[f'{var[1]}'], color=colors[var[0]])
            plt.legend(f'{var[1]}')
            plt.show()
            if save_mode:
                if not os.path.exists(f'./output/fig/{now}'):
                    os.mkdir(f'./output/fig/{now}')
                plt.savefig(f'./output/fig/{now}/{var[1]}.png')
                print('已保存')
    else:
        for var in enumerate(population_code):
            # plt.figure(figsize=(4, 4))
            plt.plot(data[f'{var[1]}'], color=colors[var[0]])
            plt.legend(f'{var[1]}')
            plt.show()
            if save_mode:
                if not os.path.exists(f'./output/fig/{now}'):
                    os.mkdir(f'./output/fig/{now}')
                plt.savefig(f'./output/fig/{now}/{var[1]}.png')
                print('已保存')

# 用于返回图例legend，判断哪个单u_i!=0
def u_mode(u1=0, u2=0, u3=0):
    tp = [0, 0, 0]
    for i in enumerate([u1, u2, u3]):
        if i[1] != 0:
            tp[i[0]] = 1
        # print(i[1])

    def sim(num):
        if num == 0:
            return '='
        else:
            return '\\neq'

    return f'u_1{sim(tp[0])}0, u_2{sim(tp[1])}0, u_3{sim(tp[2])}0'

# 控制模型 单u_i !=0 对比 基础模型
def plot_diff(base_data, model_data, population_code=None, start=0, end=72, save_mode=True, legend_mode=True, u1=0,
              u2=0, u3=0,
              save_label='test'):
    global base_column, now
    base = pd.DataFrame(base_data.values, columns=['base_S', 'base_E', 'base_I', 'base_Q', 'base_R', 'base_N'])
    bam = pd.concat((base, model_data), axis=1)
    if population_code is None:
        for var in enumerate(base_column):
            plt.figure()
            plt.plot(bam[f'{var[1]}'].iloc[start:end], color=colors[var[0] + 1])
            plt.plot(bam[f'base_{var[1]}'].iloc[start:end], linestyle='--')
            plt.xlabel('Time(days)', fontsize=15)
            if legend_mode:
                # plt.legend([f'$u_{uu}={uv}$', f'$u_{uu}=0$'])
                u_label = u_mode(u1=u1, u2=u2, u3=u3)
                plt.legend([f'${u_label}$', f'$u_1 = u_2 = u_3 =  0$'])
                plt.ylabel(f'{text[var[0]]}', fontsize=15)
                plt.ticklabel_format(style='sci', scilimits=(0, 0), axis='y')
            else:
                plt.legend([var[1], f'base_{var[1]}'])
            plt.grid(linestyle=':', alpha=0.3)
            if save_mode:
                if not os.path.exists(f'./output/fig/{save_label} {now}'):
                    os.mkdir(f'./output/fig/{save_label} {now}')
                plt.savefig(f'./output/fig/{save_label} {now}/{var[1]}_compare.png')
                print('已保存')
            plt.show()

        plt.figure()
        plt.plot(bam['V'].iloc[start:end], color=colors[7])
        plt.xlabel('Time(days)', fontsize=15)
        if legend_mode:
            # plt.legend([f'$u_{uu}={uv}$', f'${uu}=0$'])
            u_label = u_mode(u1=u1, u2=u2, u3=u3)
            plt.legend([f'${u_label}$', f'$u_1 = u_2 = u_3 =  0$'])
            plt.ylabel('Vaccinated Population (V)', fontsize=15)
            plt.ticklabel_format(style='sci', scilimits=(0, 0), axis='y')
        else:
            plt.legend('V')
        plt.grid(linestyle=':', alpha=0.3)
        if save_mode:
            plt.savefig(f'./output/fig/{save_label} {now}/V_compare.png')
            print('已保存')
        plt.show()

    # TODO: 原本想跟是上面一样做一个可以选择生成部分的，但是目前除 V 以为人群都可以
    else:
        for var in enumerate(base_column):
            # plt.figure(figsize=(4, 4))
            plt.figure()
            plt.plot(bam[f'{var[1]}'], color=colors[var[0] + 1])
            plt.plot(bam[f'base_{var[1]}'], linestyle='--')
            plt.legend([f'{var[1]}', f'base_{var[1]}'])
            if save_mode:
                if not os.path.exists(f'./output/fig/{save_label} {now}'):
                    os.mkdir(f'./output/fig/{save_label} {now}')
                plt.savefig(f'./output/fig/{save_label} {now}/{var[1]}_compare.png')
            plt.show()
        if 'V' in population_code:
            plt.figure()
            plt.plot(bam['V'], color=colors[7])
            plt.legend('V')
            if not os.path.exists(f'./output/fig/{save_label} {now}'):
                os.mkdir(f'./output/fig/{save_label} {now}')
            if save_mode:
                plt.savefig(f'./output/fig/{save_label} {now}/V_compare.png')
            plt.show()

# i_I,i_Q 时变参数散点图
def plot_scatter_figure(para_data, color_num=0, sava_mode=False):
    pp = para_data[['i_I', 'i_Q']]
    x = np.linspace(1, 72, 72)
    plt.figure()
    # plt.scatter(x,pp['i_I'])
    # plt.scatter(x,pp['i_Q'],marker='o')
    plt.plot(pp, marker='o', linestyle='', markerfacecolor='white')
    plt.ylabel('Value of parameters', fontsize=15)
    plt.xlabel('Time(days)', fontsize=15)
    plt.grid(linestyle=':', alpha=0.5)
    # plt.legend([f'${pp.name}$'], fontsize=15)
    plt.legend(pp.columns)
    if sava_mode:
        plt.savefig(f'./output/fig/scatter i_I i_Q {now}.png')
        print('已保存')
    plt.show()

# 拟合图重绘
def plot_fit(base_file_name, save_mode=False):
    base_data = pd.read_csv(base_file_name, index_col=0)
    real_data = pd.read_csv('./data/currentconfirmed.csv', header=None)
    fit_data = pd.concat((base_data['Q'], real_data.iloc[0:72, :]), axis=1)
    fit_data.columns = ['fit_data', 'real_data']
    plt.figure()
    plt.ticklabel_format(style='sci', scilimits=(0, 0), axis='y')
    plt.ylabel('Confirmed Population', fontsize=15)
    plt.xlabel('Time(days)', fontsize=15)
    plt.plot(fit_data)
    plt.legend(fit_data.columns)
    plt.grid(linestyle=':', alpha=0.3)
    if save_mode:
        plt.savefig(f'./output/fig/fit_datd_diff {now}.png')
        print('已保存')
    plt.show()


# 灵敏度分析
# e.g. para_name='beta_bd', para_changes=[0.5,0.57,0.65] ,start=40, end=60,save_label='beta_bd'
def sensitivity(para_file, para_name, para_changes, start=0, end=72, save_mode=False, save_label='test'):
    para_data = pd.DataFrame(para_file, columns=para_file.columns)
    all_data = pd.DataFrame()
    for i in range(len(para_changes)):
        para_data[f'{para_name}'] = para_changes[i]
        print(f'正在计算人群:{text[i]}')
        model_data = para2data_all_newmodel(para=para_data, u1=0, u2=0, u3=0)
        model_data.columns = [f'S_{para_name}_{para_changes[i]}', f'E_{para_name}_{para_changes[i]}',
                              f'I_{para_name}_{para_changes[i]}', f'Q_{para_name}_{para_changes[i]}',
                              f'R_{para_name}_{para_changes[i]}', f'N_{para_name}_{para_changes[i]}',
                              f'V_{para_name}_{para_changes[i]}']
        # model_data.columns = [f'S_{para_name}_{para_changes[i]}', f'E_{para_name}_{para_changes[i]}',
        #                       f'I_{para_name}_{para_changes[i]}', f'Q_{para_name}_{para_changes[i]}',
        #                       f'R_{para_name}_{para_changes[i]}', f'N_{para_name}_{para_changes[i]}']
        all_data = pd.concat((all_data, model_data), axis=1)

    for i in range(len(pop_column)):
        plt.figure()
        plt.title(f'{para_name}')
        plt.ticklabel_format(style='sci', scilimits=(0, 0), axis='y')
        plt.ylabel(f'{text[i]}', fontsize=15)
        plt.xlabel('Time(days)', fontsize=15)
        legend_list = []
        x = np.linspace(start, end, (end - start))
        for j in range(len(para_changes)):
            plt.plot(x, all_data[f'{pop_column[i]}_{para_name}_{para_changes[j]}'].iloc[start:end])
            legend_list.append(str(para_changes[j]))
        plt.grid(linestyle=':', alpha=0.3)
        plt.legend(legend_list)
        plt.xlim((start, end))
        plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

        if save_mode:
            if not os.path.exists(f'./output/fig/pc-{save_label} day-{start}-{end} {now}'):
                os.mkdir(f'./output/fig/pc-{save_label} day-{start}-{end} {now}')
            plt.savefig(f'./output/fig/pc-{save_label} day-{start}-{end} {now}/{text[i]}.png')
            print('已保存')
        plt.show()
    return all_data


# 控制模型 u_1,u_2,u_3 !=0 对比 单u_i !=0
def model_3(para_file, u_1=0, u_2=0, u_3=0, start=0, end=72, save_mode=False, save_label='test', sp_color=colors,
            line_s='-', draw=[1, 1, 1, 1]):
    para_data = pd.DataFrame(para_file, columns=para_file.columns)
    all_data = pd.DataFrame()
    u_list_1 = [u_1, 0, 0, u_1]
    u_list_2 = [0, u_2, 0, u_2]
    u_list_3 = [0, 0, u_3, u_3]
    for i in range(4):
        print(f'正在计算情况:{i}')
        if draw[i]:
            model_data = para2data_all_newmodel(para=para_data, u1=u_list_1[i], u2=u_list_2[i], u3=u_list_3[i])
        model_data.columns = [f'S_{i}', f'E_{i}', f'I_{i}', f'Q_{i}', f'R_{i}', f'N_{i}', f'V_{i}']
        all_data = pd.concat((all_data, model_data), axis=1)

    for i in range(len(pop_column)):
        plt.figure()
        plt.ticklabel_format(style='sci', scilimits=(0, 0), axis='y')
        plt.ylabel(f'{text[i]}', fontsize=15)
        plt.xlabel('Time(days)', fontsize=15)
        legend_list=[]
        for j in range(3):
            if draw[j]:
                plt.plot(all_data[[f'{pop_column[i]}_{j}']].iloc[start:end], color=sp_color[j])
                legend_list.append(f'${u_mode(u_1,u_2,u_3)}$')
        plt.plot(all_data[[f'{pop_column[i]}_{3}']].iloc[start:end], color=sp_color[3], linestyle=line_s)
        plt.grid(linestyle=':', alpha=0.3)
        # legend_list = ['$u_1\\neq 0,u_2=0,u_3=0$', '$u_1=0,u_2\\neq 0,u_3=0$', '$u_1=0,u_2=0,u_3\\neq 0$',
        #                '$u_1\\neq 0,u_2\\neq 0,u_3\\neq 0$']
        legend_list.append(str('$u_1\\neq 0,u_2\\neq 0,u_3\\neq 0$'))
        plt.legend(legend_list)
        plt.xlim((start, end))
        plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

        if save_mode:
            if not os.path.exists(f'./output/fig/3_not0 {save_label} {now} day-{start}-{end}'):
                os.mkdir(f'./output/fig/3_not0 {save_label} {now} day-{start}-{end}')
            plt.savefig(f'./output/fig/3_not0 {save_label} {now} day-{start}-{end}/{text[i]}.png')
            print('已保存')
        plt.show()

    return all_data


# TODO:实现四种模型输出其他时变参数，调整特殊参数u，输出人数，人数变化对比图

# model 1 疫苗模型 修改参数:u1 E->I
def model_vaccine(file_base_populations, file_parameters, u_1=0.0, start=0, end=72, save_mode=True):
    m_data = para2data_all_newmodel(file_name=file_parameters, u1=u_1)
    base_data = pd.read_csv(file_base_populations, index_col=0)
    plot_diff(base_data, m_data, save_mode=save_mode, legend_mode=True, u1=u_1, start=start, end=end,
              save_label='vaccine_m')
    return m_data


# model 2 人口流动模型 修改参数:u2 S->E
def model_population(file_base_populations, file_parameters, u_2=0.0, start=0, end=72, save_mode=True):
    m_data = para2data_all_newmodel(file_name=file_parameters, u2=u_2)
    base_data = pd.read_csv(file_base_populations, index_col=0)
    plot_diff(base_data, m_data, save_mode=save_mode, legend_mode=True, u2=u_2, start=start, end=end,
              save_label='population_m')
    return m_data


# model 3 核酸检测模型 修改参数:u3 I->Q
def model_nucleic(file_base_populations, file_parameters, u_3=0.0, start=0, end=72, save_mode=True):
    m_data = para2data_all_newmodel(file_name=file_parameters, u3=u_3)
    base_data = pd.read_csv(file_base_populations, index_col=0)
    plot_diff(base_data, m_data, save_mode=save_mode, legend_mode=True, u3=u_3, start=start, end=end,
              save_label='nucleic_m')
    return m_data


# model 4 口罩模型 修改参数:u4 E->I
def model_mask():
    pass
