import time
from time import strftime, gmtime

import matplotlib.pyplot as plt
import pandas as pd

tic = time.perf_counter()
time.sleep(1)
toc = time.perf_counter()

t = toc - tic
print(strftime("%H:%M:%S", gmtime(t)))

def shit(u=0):
    print(u)

shit(1)
shit()

colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
          '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
from para2data import para2data_all_newmodel
model_data = para2data_all_newmodel('data/base_model_para_all.csv', u1=0.1)
model = pd.DataFrame(model_data.values,columns=['S', 'E', 'I', 'Q', 'R', 'N', 'V'])
base_data = pd.read_csv('data/base_model_population.csv',index_col=0)
base = pd.DataFrame(base_data.values,columns=['base_S', 'base_E', 'base_I', 'base_Q', 'base_R', 'base_N'])
bam = pd.concat((base,model_data),axis=1)
plt.figure(figsize=(4,3))
plt.plot(bam['Q'],color=colors[3])
plt.plot(bam['base_Q'],linestyle='--')
plt.legend(['Q','base_Q'])
plt.show()
u1 = 1
u2 = 2
u3 = 3
for i in enumerate([u1,u2,u3]):
    print(i)
print(f'{None}')
