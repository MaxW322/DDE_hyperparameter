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
eng = matlab.engine.start_matlab()
tf = eng.isprime(37)

# TODO:实现四种模型输出其他时变参数，调整特殊参数u，输出人数，人数变化对比图

# model 1 疫苗模型 修改参数:u1 E->I
def model_vaccine():
    pass

# model 2 人口流动模型 修改参数:u2 S->E
def model_population():
    pass

# model 3 核酸检测模型 修改参数:u3 I->Q
def model_nucleic():
    pass

# model 4 口罩模型 修改参数:u4 E->I
def model_mask():
    pass



if __name__ == "__main__":
    pass