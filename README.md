# opt_dde_covid

这个项目是用于解决需要参数寻优拟合真实数据的dde问题

## 基础模型solution

使用hyper opt作为超参数寻优工具，超参数导入matlab中 **(para_all_divide.m)** 生成dde方程组中，matlab的dde23计算出数值解，并求出与真实值的rmse返回到python中，返回给opt函数作为贝叶斯分析最优参数的考据。

## 基础模型 二参数拟合 solution

同上，将基础模型超参数寻优的参数只保留 $ i_I,i_Q $ ,通过 **para_all_divide_2para.m**导入matlab中，其他参数通过第一次非时变定参数拟合得出
