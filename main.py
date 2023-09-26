import pandas as pd
from functions import getAzureKey
from functions import GetFacts
from functions import GetDims

user = getAzureKey('KV-DENA', 'KVK-API-HUKAS-PROD')
ww = getAzureKey('KV-DENA', 'KVW-API-HUKAS-PROD')


F_FILES = GetFacts(user, ww, 'Files')

# Add CASSES
output = GetDims(user, ww, table= 'Casess', sub_table = 'File')
D_CASESS = output[1]
D_CASESS.drop_duplicates(inplace=True)
temp = output[0].drop_duplicates()
temp = temp[temp['ID'] != 'K0']
F_FILES = pd.merge(F_FILES, temp,'left')

# Add REQUESTERTYPE
output = GetDims(user, ww, table= 'RequesterTypes', sub_table = 'Casess')
D_REQUESTER_TYPES = output[1]
D_REQUESTER_TYPES.drop_duplicates(inplace=True)
temp = output[0].drop_duplicates()
temp = temp[temp['ID'] != 'K0']
temp.rename(columns={'D_REQUESTERTYPES_ID': 'ID', 'ID' : 'CASES_ID'},inplace=True)
D_REQUESTER_TYPES = pd.merge(D_REQUESTER_TYPES,temp)

# Add BEHANDELENDEPARTIJS
output = GetDims(user, ww, table= 'BehandelendePartijs', sub_table = 'Files')
D_BEHANDELENDEPARTIJS = output[1]
D_BEHANDELENDEPARTIJS.drop_duplicates(inplace=True)
temp = output[0].drop_duplicates()
temp = temp[temp['ID'] != 'K0']
F_FILES = pd.merge(F_FILES, temp,'left')

# Add STATUS
output = GetDims(user, ww, table= 'Statuss', sub_table = 'Files')
D_STATUSS = output[1]
D_STATUSS.drop_duplicates(inplace=True)
temp = output[0].drop_duplicates()
temp = temp[temp['ID'] != 'K0']
F_FILES = pd.merge(F_FILES, temp,'left')

# Mutatie tabel maken
output = GetDims(user, ww, table= 'StatusChanges', sub_table = 'File')
D_STATUS_CHANGES = output[1]
temp = output[0].drop_duplicates()
temp = temp[temp['ID'] != 'K0']
temp.rename(columns={'D_STATUSCHANGES_ID': 'ID', 'ID' : 'FILE_ID'},inplace=True)
D_STATUS_CHANGES = pd.merge(D_STATUS_CHANGES,temp)

# Add DECISSIONS
output = GetDims(user, ww, table= 'Decisions', sub_table = 'File')
D_DECISIONS = output[1]
temp = output[0].drop_duplicates()
temp = temp[temp['ID'] != 'K0']
temp.rename(columns={'D_DECISIONS_ID': 'ID', 'ID' : 'FILE_ID'},inplace=True)
D_DECISIONS = pd.merge(D_DECISIONS,temp)


del output, user, ww, temp
F_FILES.to_csv(f'outputtables/F_FILES.csv',index=False, sep =';', encoding='utf-8-sig')
D_BEHANDELENDEPARTIJS.to_csv(f'outputtables/D_BEHANDELENDEPARTIJS.csv',index=False, sep =';', encoding='utf-8-sig')
D_REQUESTER_TYPES.to_csv(f'outputtables/D_REQUESTER_TYPES.csv',index=False, sep =';', encoding='utf-8-sig')
D_STATUSS.to_csv(f'outputtables/D_STATUSS.csv',index=False, sep =';', encoding='utf-8-sig')
D_STATUS_CHANGES.to_csv(f'outputtables/D_STATUS_CHANGES.csv',index=False, sep =';', encoding='utf-8-sig')
D_CASESS.to_csv(f'outputtables/D_CASESS.csv',index=False, sep =';', encoding='utf-8-sig')
D_DECISIONS.to_csv(f'outputtables/D_DECISIONS.csv',index=False, sep =';', encoding='utf-8-sig')







