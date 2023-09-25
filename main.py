
import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
# from library import HUKAS_TABLES

# import os
# # Get environment variables
# user = os.getenv('KVK-API-HUKAS-PROD')
# ww = os.environ.get('KVW-API-HUKAS-PROD')

#################
def getAzureKey(vault, key):
    '''Retrieve keys from the Azure keyvault with the vault name and key name'''
    from azure.keyvault.secrets import SecretClient
    from azure.identity import AzurePowerShellCredential
    
    #get credentials
    credential = AzurePowerShellCredential() 
    client = SecretClient(vault_url=f'https://{vault}.vault.azure.net', credential=credential)
    retrieved_secret = client.get_secret(name=key)
    
    return retrieved_secret.value

user = getAzureKey('KV-DENA', 'KVK-API-HUKAS-PROD')
ww = getAzureKey('KV-DENA', 'KVW-API-HUKAS-PROD')

# Get FACT

def IDtoSTR(df, col):
    '''Changes data type of a column of a dataframe from int to str'''
    # Replace NA values with 0
    df[col] = df[col].fillna(0).astype('int64')
    # Add 'K' (for 'key') to ensure value is a string
    df[col] = 'K' + df[col].astype(str)

    return df

# set authorisation
def GetFacts(user, ww, table):
    auth = HTTPBasicAuth(user, ww)
    # set base URL for HUKAS
    base_url = 'https://hukas.hu.nl/odata/Hukas_OData/v1/'

    # Get main table and write to CSV
    r = requests.get(f'{base_url}{table}',
                            auth = auth).json()

    # transform response json to dataframe
    output = IDtoSTR(pd.DataFrame(r['value']),'ID')
                     
    return output



def GetDims(user, ww, table, sub_table):
    auth = HTTPBasicAuth(user, ww)

    # set base URL for HUKAS
    base_url = 'https://hukas.hu.nl/odata/Hukas_OData/v1/'

    # get record from API url
    r = requests.get(f'{base_url}{table}?$expand={sub_table}',
                    auth = auth).json()

    # transform response json to dataframe
    temp = pd.DataFrame(r['value'])
    temp = IDtoSTR(temp,'ID')

    # SET DIMENSIONS
    dim = temp.copy()
    dim.drop(columns=[sub_table],inplace=True)

    # make a list to check what the format of nested values
    list_check = temp[~temp[sub_table].isnull()][sub_table].reset_index()

    if isinstance(list_check[sub_table][0], list):
        output = temp[sub_table].explode().pipe(lambda x: pd.json_normalize(x).set_index(x.index))
    else:
        output = pd.json_normalize(temp[sub_table])

    # ID to str
    output = IDtoSTR(output,'ID')
    

    # rename ID from main table  
    temp = temp[['ID']]
    temp.rename(columns={'ID':f'D_{table}_ID'.upper()}, inplace=True)
    merge_table = pd.merge(temp, output, left_index=True, right_index=True)
    merge_table = merge_table[['ID',f'D_{table}_ID'.upper()]]

    return merge_table, dim

# Get and create FILES fact table
F_FILES = GetFacts(user, ww, 'Files')

# Get and create CASESS
output = GetDims(user, ww, table= 'Casess', sub_table = 'File')
D_CASESS = output[1]
D_CASESS.drop_duplicates(inplace=True)
temp = output[0].drop_duplicates()
temp = temp[temp['ID'] != 'K0']
F_FILES = pd.merge(F_FILES, temp,'left')

# Get and create REQUESTERTYPE table
output = GetDims(user, ww, table= 'RequesterTypes', sub_table = 'Casess')
D_REQUESTER_TYPES = output[1]
D_REQUESTER_TYPES.drop_duplicates(inplace=True)
temp = output[0].drop_duplicates()
temp = temp[temp['ID'] != 'K0']
temp.rename(columns={'D_REQUESTERTYPES_ID': 'ID', 'ID' : 'CASES_ID'},inplace=True)
D_REQUESTER_TYPES = pd.merge(D_REQUESTER_TYPES,temp)

# Get and create  BEHANDELENDEPARTIJS
output = GetDims(user, ww, table= 'BehandelendePartijs', sub_table = 'Files')
D_BEHANDELENDEPARTIJS = output[1]
D_BEHANDELENDEPARTIJS.drop_duplicates(inplace=True)
temp = output[0].drop_duplicates()
temp = temp[temp['ID'] != 'K0']
F_FILES = pd.merge(F_FILES, temp,'left')

# Get and create STATUS
output = GetDims(user, ww, table= 'Statuss', sub_table = 'Files')
D_STATUSS = output[1]
D_STATUSS.drop_duplicates(inplace=True)
temp = output[0].drop_duplicates()
temp = temp[temp['ID'] != 'K0']
F_FILES = pd.merge(F_FILES, temp,'left')

# Get and create Mutatie table
output = GetDims(user, ww, table= 'StatusChanges', sub_table = 'File')
D_STATUS_CHANGES = output[1]
temp = output[0].drop_duplicates()
temp = temp[temp['ID'] != 'K0']
temp.rename(columns={'D_STATUSCHANGES_ID': 'ID', 'ID' : 'FILE_ID'},inplace=True)
D_STATUS_CHANGES = pd.merge(D_STATUS_CHANGES,temp)

# Get and create DECISSIONS table
output = GetDims(user, ww, table= 'Decisions', sub_table = 'File')
D_DECISIONS = output[1]
temp = output[0].drop_duplicates()
temp = temp[temp['ID'] != 'K0']
temp.rename(columns={'D_DECISIONS_ID': 'ID', 'ID' : 'FILE_ID'},inplace=True)
D_DECISIONS = pd.merge(D_DECISIONS,temp)

# Write tables to csv files
del output, user, ww, temp
F_FILES.to_csv(f'outputtables/F_FILES.csv',index=False, sep =';', encoding='utf-8-sig')
D_BEHANDELENDEPARTIJS.to_csv(f'outputtables/D_BEHANDELENDEPARTIJS.csv',index=False, sep =';', encoding='utf-8-sig')
D_REQUESTER_TYPES.to_csv(f'outputtables/D_REQUESTER_TYPES.csv',index=False, sep =';', encoding='utf-8-sig')
D_STATUSS.to_csv(f'outputtables/D_STATUSS.csv',index=False, sep =';', encoding='utf-8-sig')
D_STATUS_CHANGES.to_csv(f'outputtables/D_STATUS_CHANGES.csv',index=False, sep =';', encoding='utf-8-sig')
D_CASESS.to_csv(f'outputtables/D_CASESS.csv',index=False, sep =';', encoding='utf-8-sig')
D_DECISIONS.to_csv(f'outputtables/D_DECISIONS.csv',index=False, sep =';', encoding='utf-8-sig')







