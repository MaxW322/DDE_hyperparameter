import matplotlib.pyplot as plt
import pandas as pd

from __para2data import para2data_all_newmodel
from __plot_output import plot_diff



# TODO:实现四种模型输出其他时变参数，调整特殊参数u，输出人数，人数变化对比图

# model 1 疫苗模型 修改参数:u1 E->I
def model_vaccine(file_base_populations, file_parameters,u_1=0.0):
    m_data = para2data_all_newmodel(file_parameters,u1=u_1)
    base_data = pd.read_csv(file_base_populations, index_col=0)
    plot_diff(base_data,m_data,save_mode=True,legend_mode=True,u1=u_1,save_label='vaccine_m')
    return m_data

# model 2 人口流动模型 修改参数:u2 S->E
def model_population(file_base_populations, file_parameters,u_2=0.0):
    m_data = para2data_all_newmodel(file_parameters, u2=u_2)
    base_data = pd.read_csv(file_base_populations, index_col=0)
    plot_diff(base_data, m_data, save_mode=True, legend_mode=True, u2=u_2,save_label='population_m')
    return m_data

# model 3 核酸检测模型 修改参数:u3 I->Q
def model_nucleic(file_base_populations, file_parameters,u_3=0.0):
    m_data = para2data_all_newmodel(file_parameters, u3=u_3)
    base_data = pd.read_csv(file_base_populations, index_col=0)
    plot_diff(base_data, m_data, save_mode=True, legend_mode=True, u3=u_3,save_label='nucleic_m')
    return m_data

# model 4 口罩模型 修改参数:u4 E->I
def model_mask():
    pass



if __name__ == "__main__":
    file_para = 'data/base_model_para_all.csv'
    file_base = 'data/base_model_population.csv'

    model_vaccine(file_base,file_para,0.1)
    model_population(file_base, file_para, 0.5)
    model_nucleic(file_base, file_para, 0.7)
    # test
    # model_vaccine(file_base,file_para,0.1)
    # model_data = para2data_all_newmodel(file_para, u1=0.1)
    # base_data = pd.read_csv(file_base, index_col=0)
    # plot_diff(base_data,model_data)
    # plot_diff(base_data,model_data,save_mode=True,legend_mode=True,u1=0.1)
