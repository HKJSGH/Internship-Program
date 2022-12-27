import numpy as np
import pandas as pd
import os
import itertools

result_path = 'F:\\yifan\\Project\\Code\\100025102.csv'
result = pd.DataFrame(pd.read_csv('F:\\yifan\\Project\\Code\\100025102.csv'))
f_sample_candidate = result.columns.values.tolist()
# f_sample_candidate.remove(join_columns_name)
f_sample_can = list(itertools.permutations(f_sample_candidate, 2))
f_sample_candidate
f_sample_can
f_sample = []
for n in range(len(f_sample_can)):
    f_test = pd.DataFrame(pd.read_csv(result_path,usecols=f_sample_can[n]))
    f_test_dict = f_test.set_index(f_sample_can[n][0]).T.to_dict('list')
    for i in f_test_dict.values():
        if (len(i)) != 1:
            print('maybe_f_sample')
            f_test_sample = f_test.sample(n=20,axis=0)
            f_test_sample_dict = f_test_sample.set_index(f_sample_can[n][0]).T.to_dict('list')
            for j in f_test_sample_dict.values():
                if (len(j)) == 1:
                    f_sample.append(f_sample_can[n])
                    print('f_sample')
                    break
pd.DataFrame(f_sample).to_csv(sample_path_f + '\\' + 'f_sample.csv',index=False)

[('Year','Month')]
f_test = pd.DataFrame(pd.read_csv(result_path,usecols=('Year','Month')))
f_test_dict = f_test.set_index('Year').T.to_dict('list')
f_test_dict