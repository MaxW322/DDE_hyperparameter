import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
from datetime import datetime

# TODO: 输入Dataframe，输出每种人群的变化图
# TODO: 输入Dataframe，输出每种人群与基础模型拟合的比较图
# TODO: 锁定人群排序: ['S', 'E', 'I', 'Q', 'R', 'N', 'V']

text = ['Susceptible population', 'Exposed population', 'Infected population', 'Confirmed population', 'Recovery population']
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
            plt.plot(data[f'{var[1]}'],color=colors[var[0]])
            plt.legend(f'{var[1]}')
            plt.show()
            if save_mode:
                if not os.path.exists(f'./output/fig/{now}'):
                    os.mkdir(f'./output/fig/{now}')
                plt.savefig(f'./output/fig/{now}/{var[1]}.png')
    else:
        for var in enumerate(population_code):
            # plt.figure(figsize=(4, 4))
            plt.plot(data[f'{var[1]}'],color=colors[var[0]])
            plt.legend(f'{var[1]}')
            plt.show()
            if save_mode:
                if not os.path.exists(f'./output/fig/{now}'):
                    os.mkdir(f'./output/fig/{now}')
                plt.savefig(f'./output/fig/{now}/{var[1]}.png')


def plot_diff(base_data, model_data, population_code=None, save_mode=True, legend_mode=False,u1=0,u2=0,u3=0,save_label='test'):
    global base_column, now
    base = pd.DataFrame(base_data.values, columns=['base_S', 'base_E', 'base_I', 'base_Q', 'base_R', 'base_N'])
    bam = pd.concat((base, model_data), axis=1)
    if population_code is None:
        for var in enumerate(base_column):
            plt.figure()
            plt.plot(bam[f'{var[1]}'],color=colors[var[0]+1])
            plt.plot(bam[f'base_{var[1]}'],linestyle='--')
            plt.xlabel('Time(days)', fontsize=15)
            if legend_mode:
                uu = 1
                uv = 0
                for i in enumerate([u1,u2,u3]):
                    if i[1] != 0:
                        uu = i[0]+1
                        uv = i[1]
                # plt.legend([f'$u_{uu}={uv}$', f'$u_{uu}=0$'])
                plt.legend([f'$u_{uu} \\neq 0$', f'$u_{uu} = 0$'])
                plt.ylabel(f'{var[1]} population', fontsize=15)
            else:
                plt.legend([var[1], f'base_{var[1]}'])
            plt.grid(linestyle=':',alpha=0.2)
            if save_mode:
                if not os.path.exists(f'./output/fig/{save_label} {now}'):
                    os.mkdir(f'./output/fig/{save_label} {now}')
                plt.savefig(f'./output/fig/{save_label} {now}/{var[1]}_compare.png')
                plt.show()

        plt.figure()
        plt.plot(bam['V'], color=colors[7])
        plt.xlabel('Time(days)', fontsize=15)
        if legend_mode:
            uu = 1
            uv = 0
            for i in enumerate([u1, u2, u3]):
                if i[1] != 0:
                    uu = i[0] + 1
                    uv = i[1]
            # plt.legend([f'$u_{uu}={uv}$', f'${uu}=0$'])
            plt.legend([f'$u_{uu} \\neq 0$', f'${uu} = 0$'])
            plt.ylabel('V population', fontsize=15)
        else:
            plt.legend('V')
        plt.grid(linestyle=':', alpha=0.2)
        if save_mode:
            plt.savefig(f'./output/fig/{save_label} {now}/V_compare.png')
        plt.show()

    # TODO: 原本想跟是上面一样做一个可以选择生成部分的，但是目前除 V 以为人群都可以
    else:
        for var in enumerate(base_column):
            # plt.figure(figsize=(4, 4))
            plt.figure()
            plt.plot(bam[f'{var[1]}'],color=colors[var[0]+1])
            plt.plot(bam[f'base_{var[1]}'],linestyle='--')
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


