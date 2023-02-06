from  scipy.stats import chi2_contingency
import numpy as np
import pandas as pd
import os

File_name = '101041335'
head_path = 'F:\\yifan\Project\\'
test_path = head_path + 'FD_test\\' + File_name +'.csv'
t_path = head_path + 'TF_sample\\' + File_name + '\\t_sample.csv' 
f_path = head_path + 'TF_sample\\' + File_name + '\\f_sample.csv' 
text_file = pd.DataFrame(pd.read_csv(test_path))
f_index = pd.DataFrame(pd.read_csv(f_path))
f_name = []
for i in range(len(f_index)):
    f_name.append((f_index['0'][i],f_index['1'][i]))
f_name[0][0]
f_name[0][1]
f_name

for n in range(len(f_name)):
    crosstab = pd.crosstab(text_file[f_name[n][0]],text_file[f_name[n][1]])
    kt = chi2_contingency(crosstab) 
    print('卡方值=%.4f, p值=%.4f, 自由度=%i expected_frep=%s'%kt)

  
# file_name='F:\yifan\Project\_columns.csv'
# #names=['separ-length','separ-width','petal_length','petal_width','class']
# data=pd.read_csv(file_name)
# print(data)
# print(data.shape)
# data_full = data.iloc[0:20,[1,4,5,8,10,11]]
# print(data_full)
# print(data_full.shape)
# data_1 = pd.crosstab(data_full['TableID'],data_full['ExplicitDataType'])
# print(data_1)
# kt = chi2_contingency(data_1)
# print('卡方值=%.4f, p值=%.4f, 自由度=%i expected_frep=%s'%kt)

# column_name = ['TableID','ExplicitDataType','InferredDataType','IsHidden','IsUnique','IsKey']
# for i in column_name:
#     for j in column_name:
#         kt = chi2_contingency(pd.crosstab(data_full[i],data_full[j]))
#         print('卡方值=%.4f, p值=%.4f, 自由度=%i expected_frep=%s'%kt)
        
t_sample_path = 'F:\\yifan\Project\TF_sample'
t_sample_names = os.listdir(t_sample_path)

t_len = []

for i in t_sample_names:
    try:
        t_path = t_sample_path + '\\' + i + '\\t_sample.csv'
        new_len = len(pd.read_csv(t_path))
        t_len.append(new_len)
    except:
        t_len.append(0)
        pass
    
# t_path = 'F:\yifan\Project\TF_sample\\100071583\\t_sample.csv'
# len(pd.read_csv(t_path))

t_mean_number = sum(t_len)/len(t_len)
print(t_mean_number)