from sklearn import metrics
import numpy as np
import pandas as pd
import os
import eventlet
import time
from func_timeout import func_set_timeout
import func_timeout
import matplotlib.pyplot as plt


File_name = '100025102'
p = 0.05
head_path = 'F:\\yifan\Project\\'
test_path = head_path + 'FD_test\\' + File_name +'.csv'
t_path = head_path + 'TF_sample\\' + File_name + '\\t_sample.csv' 
f_path = head_path + 'TF_sample\\' + File_name + '\\f_sample.csv' 
text_file = pd.DataFrame(pd.read_csv(test_path))
f_index = pd.DataFrame(pd.read_csv(f_path))
f_name = []
t_index = pd.DataFrame(pd.read_csv(t_path))
t_name = []
TP = 0
Positive = 0
for i in range(len(f_index)):
    f_name.append((f_index['0'][i],f_index['1'][i]))
for i in range(len(t_index)):
    t_name.append((t_index['0'][i],t_index['1'][i]))    
columns_pairs = f_name + t_name 
for n in range(len(columns_pairs)):
    #################################
    a = []
    a_num = []
    for i in text_file[columns_pairs[n][0]]:
        if i not in a:
            a.append(i)
        a_num.append(a.index(i))
    b = []
    b_num = []
    for i in text_file[columns_pairs[n][1]]:
        if i not in b:
            b.append(i)
        b_num.append(b.index(i))
    #################################
    result_NMI = metrics.normalized_mutual_info_score(a_num,b_num)  
    if result_NMI >= 1-p:
        Positive += 1
        if columns_pairs[n] in t_name:
            TP += 1
            print(columns_pairs[n])
    # if result_NMI >= 1-p and columns_pairs[n] in t_name:
    #     TP += 1
            
print('Precision',TP/Positive)  
print('Recall',TP/len(t_name)) 
f_name
t_name
columns_pairs[0]
print(columns_pairs[0])
len(columns_pairs)
plist = np.arange(0,0.5,0.05)

# dict0 = {}
# dict1 = {}
# for n in range(len(f_name)):
#     count0 = 0
#     count1 = 0
#     for l in range(len(text_file)):  
#         k0 = text_file[f_name[n][0]][l]
#         k1 = text_file[f_name[n][1]][l]
#         if k0 not in dict0.keys():
#                 dict0[k0] = count0
#                 count0 += 1
#         if k1 not in dict1.keys():
#                 dict1[k1] = count1
#                 count1 += 1
#     list0 = dict0.values()
#     list1 = dict1.values()
#     result_NMI = metrics.normalized_mutual_info_score(list0,list1)
#     if result_NMI <= 0.05:
#         TN += 1
    
