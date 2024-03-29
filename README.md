<div align="center">
<h1>
基于hyper opt超参数优化的，求带有时滞项的微分方程组(DDE)数值解
</h1>
</div>

## 实现

这个项目是用于解决需要参数寻优拟合真实数据的dde参数问题

实现方法：
通过调用`matlab.engine`，将参数传入MATLAB的dde23数值求解器中进行求解，返回数值解与真实值的RMSE
到Python中的opt函数，使用贝叶斯决策树的方式调整参数，重复以上过程得到最优参数。

## 基础模型solution

### 基础模型超参数寻优脚本

    Python端:
    _hper_2p.py
    _hyper_all_divide_outputall.py

    MATLAB端:
    para.m                      定值参数
    para_all_divide.m           全时变参数 
    para_all_divide_2para.m     部分时变参数(i_I,i_Q)

为了使拟合的效果最佳，除了定值参数的model，还编写了时变参数的model以达到更好的效果

例子:
`hyper_all_divide_outputall.py`使用hyper opt作为超参数寻优工具，超参数导入matlab中 **(para_all_divide.m)**
生成dde方程组中，matlab的dde23计算出数值解，并求出与真实值的rmse返回到python中，返回给opt函数作为贝叶斯分析最优参数的考据。

### 参数导入求数值解 控制模型 对比图绘制
    
    Pytho端：
    __para2data.py              参数导入求数值解 
    __plot_output.py            对比图绘制
    _control_model.py           控制模型(疫苗模型,人口流动模型,核酸检测模型, 口罩模型(废弃))

    MATLAB端:                   
    fit_output_all.m            参数导入输出所有人群的变化数据
    fit_output_all_new_model.m  参数导入,控制模型参数导入(u1,u2,u3),输出所有人群的变化数据

### 对比图绘制图例

<img alt="Population S example" src="https://github.com/MaxW322/opt_dde_covid/blob/main/output/fig/nucleic_m%202023-03-11%2013.30.27/S_compare.png" title="S example" width="400" height="300"/>

<img alt="Population S example" src="D:\.PycharmProj\covid_project\output\fig\nucleic_m 2023-03-11 13.30.27\S_compare.png" title="S example" width="400" height="300"/>

### 基础模型 二参数拟合 solution 说明

同上，将基础模型超参数寻优的参数只保留 $ i_I,i_Q $ ,通过 **para_all_divide_2para.m**导入matlab中，其他参数通过第一次非时变定参数拟合得出
