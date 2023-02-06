import numpy as np
import pandas as pd
import os
import itertools
import shutil
import random
from func_timeout import func_set_timeout

@func_set_timeout(15)
def f_sample_generate(File_number):
    sample_path = 'F:\\yifan\Project\TF_sample\\'
    sample_path_file = sample_path + File_number
    result_path =  'F:\\yifan\Project\FD_test\\' + File_number +'.csv'
    result = pd.DataFrame(pd.read_csv(result_path,low_memory=False))
    if len(result) <= 100:
        shutil.rmtree(sample_path + File_number)
        # print('samples < 100')
        print('delete:',File_number)
        # return
    f_sample_candidate = result.columns.values.tolist()
    if len(f_sample_candidate) > 10:
        f_sample_candidate = random.sample(f_sample_candidate, 10)
    # f_sample_candidate.remove(join_columns_name)
    f_sample_can = list(itertools.permutations(f_sample_candidate, 2))
    f_sample = []
    for n in range(len(f_sample_can)):
        f_test = pd.DataFrame(pd.read_csv(result_path,usecols=f_sample_can[n],low_memory=False))
        # f_test = f_test[pd.isnull(f_test[f_sample_can[n][0]])==False] 
        # f_test = f_test[pd.isnull(f_test[f_sample_can[n][1]])==False]      
        # f_test_dict = f_test.set_index(f_sample_can[n][0]).T.to_dict('list')
        f_test_dict = {}
        for l in range(len(f_test)):
            k = f_test[f_sample_can[n][0]][l]
            v = f_test[f_sample_can[n][1]][l]
            if pd.isnull(k) == False and pd.isnull(v) == False:
                if k not in f_test_dict.keys():
                    f_test_dict[k] = []
                if v not in f_test_dict[k]:
                    f_test_dict[k].append(v)    
        for i in f_test_dict.values():
            # print(len(i))
            if (len(i)) != 1:
                # print('1) not key-value',len(i))
                f_test_sample = f_test.sample(n=100,axis=0)
                f_test_sample = f_test_sample.reset_index(drop=True) 
                f_test_sample_dict = {}
                #########sample dict
                for l in range(len(f_test_sample)):
                    k = f_test_sample[f_sample_can[n][0]][l]
                    v = f_test_sample[f_sample_can[n][1]][l]
                    if pd.isnull(k) == False and pd.isnull(v) == False:
                        if k not in f_test_sample_dict.keys():
                            f_test_sample_dict[k] = []                
                        if v not in f_test_sample_dict[k]:
                            f_test_sample_dict[k].append(v) 
                ################           
                f_token = True
                if f_test_sample_dict == {}:
                    f_token = False
                else:
                    for j in f_test_sample_dict.values():
                        if len(j) != 1:
                            # print('2) not key-value',len(j),f_sample_can[n])
                            f_token = False
                            break
                        # else:
                        #      print('2) key-value',len(j))
                        # print(len(j))
                if f_token:
                    f_sample.append(f_sample_can[n])
                    print('f_sample',f_sample_can[n])
                break    
    if f_sample != []:
        pd.DataFrame(f_sample).to_csv(sample_path_file + '\\' + 'f_sample.csv',index=False)
    else:
        shutil.rmtree(sample_path + File_number) 
        # print('No f_sample')
        print('delete:',i)



datasets = 'F:\yifan\Project\TF_sample'
data_test_name = os.listdir(datasets)
for i in data_test_name:
    sample_path = 'F:\\yifan\Project\TF_sample\\'
    try:
        f_sample_generate(i)
    except:
        shutil.rmtree(sample_path + i) 
        print('delete:',i)
        pass
    