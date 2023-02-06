import numpy as np
import pandas as pd
import os
import itertools

File_number = '100025102'
path_head = 'F:\\yeye\\bi.data\data_extracted_from_flow_run1_2022_09_01.processed.deduped\data_extracted_from_flow_run1_2022_09_01.processed.deduped\\'
result_path_head = 'F:\\yifan\Project\FD_test\\'
sample_path = 'F:\\yifan\Project\TF_sample\\'
Relationships_path = path_head + File_number + '\\_relationships.csv'
names_relationships=['FromTableID','FromColumnID','ToTableID','ToColumnID']
relationships = pd.DataFrame(pd.read_csv(Relationships_path,usecols=names_relationships))
relationships_name = relationships.copy(deep=False)

Table_path = path_head + File_number + '\\_tables.csv'
names_table=['ID','Name']
table = pd.DataFrame(pd.read_csv(Table_path,usecols=names_table))
table_dict = table.set_index('ID').T.to_dict('list')

Columns_path = path_head + File_number + '\\_columns.csv'
names_columns=['ID','TableID','ExplicitName','InferredName']
columns = pd.DataFrame(pd.read_csv(Columns_path,usecols=names_columns))
names_columns_ExplicitName=['ID','ExplicitName']
names_columns_InferredName=['ID','InferredName']
columns_port_ExplicitName = pd.DataFrame(pd.read_csv(Columns_path,usecols=names_columns_ExplicitName))
columns_port_InferredName = pd.DataFrame(pd.read_csv(Columns_path,usecols=names_columns_InferredName))
columns_dict_ExplicitName = columns_port_ExplicitName.set_index('ID').T.to_dict('list')
columns_dict_InferredName = columns_port_InferredName.set_index('ID').T.to_dict('list')

for i in range(len(relationships['FromTableID'])): 
        relationships_name['FromTableID'][i] = table_dict[relationships['FromTableID'][i]][0] 
        relationships_name['ToTableID'][i] = table_dict[relationships['ToTableID'][i]][0] 
        if pd.isnull(columns_dict_InferredName[relationships_name['FromColumnID'][i]][0]):
            relationships_name['FromColumnID'][i] = columns_dict_ExplicitName[relationships_name['FromColumnID'][i]][0]
        else:
            relationships_name['FromColumnID'][i] = columns_dict_InferredName[relationships_name['FromColumnID'][i]][0]
        if pd.isnull(columns_dict_InferredName[relationships_name['ToColumnID'][i]][0]):
            relationships_name['ToColumnID'][i] = columns_dict_ExplicitName[relationships_name['ToColumnID'][i]][0]
        else:
            relationships_name['ToColumnID'][i] = columns_dict_InferredName[relationships_name['ToColumnID'][i]][0]
pd.set_option('display.max_columns', None)

for i in range(len(relationships_name['FromTableID'])): 
    if relationships_name['FromColumnID'][i] == relationships_name['ToColumnID'][i]:
        if len(relationships_name['FromTableID'][i]) <= 50:
            if len(relationships_name['ToTableID'][i]) <= 50:
                input_value = i
                break
    else:
        input_value == 's'

########################################################################
#先从relationship中选择一个column_number作为join的key，以及对应的table_number
#再去columns.csv中用column_number找到column_name，table.csv中用table_number找到Table_path
#创造用于test的文件

row_index_rela = int(input_value)
join_columns_ID = relationships['FromColumnID'][row_index_rela]
# row_index_rela = relationships[relationships['FromColumnID'] == join_columns_ID].index.tolist()[0]
row_index_clou = columns[columns['ID'] == join_columns_ID].index.tolist()[0]
join_columns_name = columns.loc[row_index_clou]['ExplicitName']

# join_key = relationships.loc[relationships['FromColumnID']==Columns_number,['FromTableID','ToTableID','ToColumnID']]
join_key = relationships.loc[row_index_rela,['FromTableID','ToTableID','ToColumnID']]
FromTableID = join_key.loc['FromTableID'] # 代表'FromTableID'
ToColumnID = join_key.loc['ToColumnID'] # 代表'ToColumnID'
ToTableID = join_key.loc['ToTableID'] # 代表'ToTableID'

#############################
# table_many = table.loc[table['ID'] == FromColumnID,'Name'].loc[0] #Name of table_many
table_many_name = table_dict[FromTableID][0]
table_one_name = table_dict[ToTableID][0]
############################

# Fact_name = 'C:\\Users\\Hermosa\\Desktop\\Python Project\\' + File_number + '\\'+ 'FactFinalisedInvoicesDetailed' +'.csv'
table_many_path = path_head + File_number + '\\'+ table_many_name +'.csv'
table_many = pd.DataFrame(pd.read_csv(table_many_path))

table_one_path = path_head + File_number + '\\'+ table_one_name +'.csv'

table_one = pd.DataFrame(pd.read_csv(table_one_path))
sample_candidate = table_one.columns.values.tolist()
sample_candidate.remove(join_columns_name)


result = pd.merge(table_many,table_one,how="outer",on=join_columns_name)
#     result_path = path_head + File_number + '\\'
result_path = result_path_head + File_number +'.csv'
result.to_csv(result_path,index=False)


t_sample_can = [{join_columns_name,i} for i in sample_candidate]
sample_path_f = sample_path + File_number
if os.path.exists(sample_path_f) == False:
        os.mkdir(sample_path_f)
        
pd.DataFrame(t_sample_can).to_csv(sample_path_f + '\\' + 't_sample.csv',index=False)
# pd.DataFrame(f_sample).to_csv(sample_path_f + '\\' + 'f_sample.csv',index=False)      

# f_sample_candidate = result.columns.values.tolist()
# f_sample_candidate.remove(join_columns_name)
# f_sample_can = list(itertools.permutations(f_sample_candidate, 2))
# f_sample = []
# for n in range(len(f_sample_can)):
#     print(n)
#     f_test = pd.DataFrame(pd.read_csv(result_path,usecols=f_sample_can[n]))
#     # f_test_dict = f_test.set_index(f_sample_can[n][0]).T.to_dict('list')
#     f_test_dict = {}
#     for l in range(len(f_test)):
#         k = f_test[f_sample_can[n][0]][l]
#         if k not in f_test_dict.keys():
#             f_test_dict[k] = []
#         v = f_test[f_sample_can[n][1]][l]
#         if v not in f_test_dict[k]:
#             f_test_dict[k].append(v)         
#     for i in f_test_dict.values():
#         if (len(i)) != 1:
#             f_test_sample = f_test.sample(n=100,axis=0)
#             f_test_sample = f_test_sample.reset_index(drop=True) 
#             f_test_sample_dict = {}
#             #########sample dict
#             for l in range(len(f_test_sample)):
#                 k = f_test_sample[f_sample_can[n][0]][l]
#                 if k not in f_test_sample_dict.keys():
#                     f_test_sample_dict[k] = []
#                 v = f_test_sample[f_sample_can[n][1]][l]
#                 if v not in f_test_sample_dict[k]:
#                     f_test_sample_dict[k].append(v)
#             ################
#             f_token = True
#             for j in f_test_sample_dict.values():
#                 if (len(j)) != 1:
#                     f_token = False
#                     break
#             if f_token:
#                 f_sample.append(f_sample_can[n])
#                 print('f_sample')
#             break   
# pd.DataFrame(f_sample).to_csv(sample_path_f + '\\' + 'f_sample.csv',index=False)

f_test_dict = {}
n=2
f_test = pd.DataFrame(pd.read_csv(result_path,usecols=f_sample_can[n]))
for l in range(len(f_test)):
    k = f_test[f_sample_can[n][0]][l]
    if k not in f_test_dict.keys():
        f_test_dict[k] = []
    v = f_test[f_sample_can[n][1]][l]
    if v not in f_test_dict[k]:
        f_test_dict[k].append(v)

for i in f_test_dict.values():
    if (len(i)) != 1:
        print(len(i))
f_test_sample = f_test.sample(n=100,axis=0)
f_test_sample = f_test_sample.reset_index(drop=True) 
f_test_sample_dict = {}
for l in range(len(f_test_sample)):
    k = f_test_sample[f_sample_can[n][0]][l]
    if k not in f_test_sample_dict.keys():
        f_test_sample_dict[k] = []
    v = f_test_sample[f_sample_can[n][1]][l]
    if v not in f_test_sample_dict[k]:
        f_test_sample_dict[k].append(v)
f_test_sample_dict
len(f_test_sample_dict)
f_token = True
for j in f_test_sample_dict.values():
    if (len(j)) != 1:
        f_token = False
        break



        
