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

# ����matlab
eng = matlab.engine.start_matlab()
tf = eng.isprime(37)

# TODO:ʵ������ģ���������ʱ������������������u����������������仯�Ա�ͼ

# model 1 ����ģ�� �޸Ĳ���:u1 E->I
def model_vaccine():
    pass

# model 2 �˿�����ģ�� �޸Ĳ���:u2 S->E
def model_population():
    pass

# model 3 ������ģ�� �޸Ĳ���:u3 I->Q
def model_nucleic():
    pass

# model 4 ����ģ�� �޸Ĳ���:u4 E->I
def model_mask():
    pass



if __name__ == "__main__":
    pass