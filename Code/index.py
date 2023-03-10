import numpy as np
import pandas as pd
import os

File_number = '100025102'
path_head = 'F:\\yeye\\bi.data\data_extracted_from_flow_run1_2022_09_01.processed.deduped\data_extracted_from_flow_run1_2022_09_01.processed.deduped\\'
result_path = 'F:\\yifan\Project\FD_test\\'
sample_path = 'F:\\yifan\Project\TF_sample\\'
Relationships_path = path_head + File_number + '\\_relationships.csv'
names_relationships=['FromTableID','FromColumnID','ToTableID','ToColumnID']
relationships = pd.DataFrame(pd.read_csv(Relationships_path,usecols=names_relationships))
relationships_name = relationships.copy(deep=False)
# if join_choose == False:
#      join_columns_ID = np.random.choice(relationships['FromColumnID'])
# else:
#     join_columns_ID = int(input('JoinColumn:')) 
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
    relationships_name['FromTableID'][i] = table_dict[relationships['FromTableID'][i]][0] + '(' +str(relationships['FromTableID'][i]) + ')'
    relationships_name['ToTableID'][i] = table_dict[relationships['ToTableID'][i]][0] + '(' +str(relationships['ToTableID'][i]) + ')'
    if pd.isnull(columns_dict_InferredName[relationships_name['FromColumnID'][i]][0]):
            relationships_name['FromColumnID'][i] = columns_dict_ExplicitName[relationships_name['FromColumnID'][i]][0]+ '(' +str(relationships_name['FromColumnID'][i]) + ')'
    else:
            relationships_name['FromColumnID'][i] = columns_dict_InferredName[relationships_name['FromColumnID'][i]][0]+ '(' +str(relationships_name['FromColumnID'][i]) + ')'
    if pd.isnull(columns_dict_InferredName[relationships_name['ToColumnID'][i]][0]):
            relationships_name['ToColumnID'][i] = columns_dict_ExplicitName[relationships_name['ToColumnID'][i]][0]+ '(' +str(relationships_name['ToColumnID'][i]) + ')'
    else:
            relationships_name['ToColumnID'][i] = columns_dict_InferredName[relationships_name['ToColumnID'][i]][0]+ '(' +str(relationships_name['ToColumnID'][i]) + ')'
pd.set_option('display.max_columns', None)
print(relationships_name)

########################################################################
#??????relationship???????????????column_number??????join???key??????????????????table_number
#??????columns.csv??????column_number??????column_name???table.csv??????table_number??????Table_path
#????????????test?????????
input_value = 2

row_index_rela = int(input_value)
join_columns_ID = relationships['FromColumnID'][row_index_rela]
# row_index_rela = relationships[relationships['FromColumnID'] == join_columns_ID].index.tolist()[0]
row_index_clou = columns[columns['ID'] == join_columns_ID].index.tolist()[0]
join_columns_name = columns.loc[row_index_clou]['ExplicitName']

# join_key = relationships.loc[relationships['FromColumnID']==Columns_number,['FromTableID','ToTableID','ToColumnID']]
join_key = relationships.loc[row_index_rela,['FromTableID','ToTableID','ToColumnID']]
FromTableID = join_key.loc['FromTableID'] # ??????'FromTableID'
ToColumnID = join_key.loc['ToColumnID'] # ??????'ToColumnID'
ToTableID = join_key.loc['ToTableID'] # ??????'ToTableID'

#############################
# table_many = table.loc[table['ID'] == FromColumnID,'Name'].loc[0] #Name of table_many
table_many_name = table_dict[FromTableID][0]
table_one_name = table_dict[ToTableID][0]


t_sample_can = []
sample_candidate = table_one.columns.values.tolist()
sample_candidate.remove(join_columns_name)
for i in sample_candidate:
    t_sample_can.append({join_columns_name,i})
t_sample = {File_number:t_sample_can}


############################

# Fact_name = 'C:\\Users\\Hermosa\\Desktop\\Python Project\\' + File_number + '\\'+ 'FactFinalisedInvoicesDetailed' +'.csv'
table_many_path = path_head + File_number + '\\'+ table_many_name +'.csv'
table_many = pd.DataFrame(pd.read_csv(table_many_path))

table_one_path = path_head + File_number + '\\'+ table_one_name +'.csv'

table_one = pd.DataFrame(pd.read_csv(table_one_path))

result = pd.merge(table_many,table_one,how="outer",on=join_columns_name)
#     result_path = path_head + File_number + '\\'
result.to_csv(result_path + File_number +'.csv',index=False)

sample_path_f = sample_path + File_number
if os.path.exists(sample_path_f) == False:
    os.mkdir(sample_path_f)
pd.DataFrame(t_sample_can).to_csv(sample_path_f + '\\' + 't_sample.csv',index=False)

print(f'test file has been created as {result_path}' + File_number +'.csv')



