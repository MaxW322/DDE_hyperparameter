import matplotlib.pyplot as plt
import pandas as pd

from __para2data import para2data_all_newmodel
from __plot_output import *

file_para = 'data/base_model_para_all.csv'
file_base = 'data/base_model_population.csv'

base_data = pd.read_csv(file_base, index_col=0)
para_data = pd.read_csv(file_para, header=0)

if __name__ == "__main__":

    # model_data = para2data_all_newmodel(file_name=file_para, u1=0.1)

    # model_vaccine(file_base, file_para, 0.1)
    # model_population(file_base, file_para, 0.5)
    # model_nucleic(file_base, file_para, 0.7)
    # plot_scatter_figure(para_data, sava_mode=True)

    # 灵敏度分析
    # sensitivity(para_file=para_data,para_name='beta_bd',para_changes=[0.5,0.57,0.65],start=40,end=60,save_mode=True,save_label='beta_bd')
    sensitivity(para_file=para_data, para_name='beta_bd', para_changes=[0.40, 0.57, 0.70], start=40, end=60,
                save_mode=True, save_label='beta_bd')
    sensitivity(para_file=para_data, para_name='beta_iq', para_changes=[0.0005, 0.0013, 0.0020], start=16, end=40,
                save_mode=True, save_label='beta_iq')
    sensitivity(para_file=para_data, para_name='beta_qr', para_changes=[0.400, 0.764, 0.900], start=30, end=40,
                save_mode=True, save_label='beta_qr')
    sensitivity(para_file=para_data, para_name='beta_ir', para_changes=[0.40, 0.52, 0.70], start=30, end=60,
                save_mode=True, save_label='beta_ir')


    # 拟合图重绘
    plot_fit(file_base, save_mode=True)
    # i_I,i_Q 时变参数散点图
    plot_scatter_figure(para_data, sava_mode=True)

    # 控制模型 单独u_i != 0
    model_vaccine(file_base, file_para, 0.1, start=0, end=64, save_mode=True)
    model_population(file_base, file_para, 0.5, start=0, end=64, save_mode=True)
    model_nucleic(file_base, file_para, 0.0001, start=0, end=64, save_mode=True)

    # 控制模型 u_1,u_2,u_3 !=0 对比 u_1!=0
    model3 = model_3(para_file=para_data, u_1=0.1, u_2=0.5, u_3=0.0001, start=0, end=64, save_mode=True,
                     save_label='model_3',line_s='--',draw=[1,0,0,1])

    # test,sp_color=['#d55fde','#a449ab','#733377','#7144aa']
    # model_vaccine(file_base,file_para,0.1)

    # plot_scatter_figure(para_data, sava_mode=True)
    # plot_diff(base_data,model_data)
    # plot_diff(base_data, model_data, save_mode=False, legend_mode=True, u1=0.1)
    # plot_fit(file_base, save_mode=False)
