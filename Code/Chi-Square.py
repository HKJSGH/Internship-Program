from  scipy.stats import chi2_contingency
import numpy as np
import pandas as pd
import os
import eventlet
import time
from func_timeout import func_set_timeout
import func_timeout

@func_set_timeout(3)
def chi_score(File_name):
    head_path = 'F:\\yifan\Project\\'
    test_path = head_path + 'FD_test\\' + File_name +'.csv'
    t_path = head_path + 'TF_sample\\' + File_name + '\\t_sample.csv' 
    f_path = head_path + 'TF_sample\\' + File_name + '\\f_sample.csv' 
    text_file = pd.DataFrame(pd.read_csv(test_path))
    f_index = pd.DataFrame(pd.read_csv(f_path))
    f_name = []
    p = 0.05
    TN = 0
    for i in range(len(f_index)):
        f_name.append((f_index['0'][i],f_index['1'][i]))
    for n in range(len(f_name)):
        crosstab = pd.crosstab(text_file[f_name[n][0]],text_file[f_name[n][1]])
        P_value = chi2_contingency(crosstab)[1]
        if P_value >= p:
                TN += 1
    # kt = chi2_contingency(crosstab)
    print('Recall',TN/len(f_name))  
    return(TN/len(f_name))
    # print('卡方值=%.4f, p值=%.4f, 自由度=%i expected_frep=%s'%kt)

@func_set_timeout(3)
def chi_score_t(File_name):
    head_path = 'F:\\yifan\Project\\'
    test_path = head_path + 'FD_test\\' + File_name +'.csv'
    t_path = head_path + 'TF_sample\\' + File_name + '\\t_sample.csv' 
    f_path = head_path + 'TF_sample\\' + File_name + '\\f_sample.csv' 
    text_file = pd.DataFrame(pd.read_csv(test_path))
    t_index = pd.DataFrame(pd.read_csv(t_path))
    t_name = []
    p = 0.05
    TN = 0
    for i in range(len(t_index)):
        t_name.append((t_index['0'][i],t_index['1'][i]))
    for n in range(len(t_name)):
        crosstab = pd.crosstab(text_file[t_name[n][0]],text_file[t_name[n][1]])
        P_value = chi2_contingency(crosstab)[1]
        if P_value <= p:
                TN += 1
    # kt = chi2_contingency(crosstab)
    print('Recall',TN/len(t_name))  
    return(TN/len(t_name))
    # print('卡方值=%.4f, p值=%.4f, 自由度=%i expected_frep=%s'%kt)

chi_score('100848939')

datasets = 'F:\yifan\Project\TF_sample'
data_test_name = os.listdir(datasets)[0:125]
recall_list=[]

for i in data_test_name:
    try:
        recall_list.append(chi_score_t(i))
    except:
        pass
recall_sum = 0.0
count_sum = 0
for i in range(len(recall_list)):
    if recall_list[i] != None:
        recall_sum += recall_list[i]
        count_sum += 1

print(recall_sum/count_sum)