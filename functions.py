#################
def getAzureKey(vault, key):
    '''Retrieve keys from the Azure keyvault with the vault name and key name'''
    from azure.keyvault.secrets import SecretClient
    from azure.identity import AzurePowerShellCredential
    from azure.identity import DefaultAzureCredential
    
    credential = DefaultAzureCredential() 

    
    #get credentials
    credential = AzurePowerShellCredential() 
    client = SecretClient(vault_url=f'https://{vault}.vault.azure.net', credential=credential)
    retrieved_secret = client.get_secret(name=key)
    
    return retrieved_secret.value


# Get FACT
# set autherisation
def IDtoSTR(df, col):
    df[col] = df[col].fillna(0).astype('int64')
    df[col] = 'K' + df[col].astype(str)

    return df


def GetFacts(user, ww, table):
    from requests.auth import HTTPBasicAuth
    import pandas as pd
    import requests
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
    from requests.auth import HTTPBasicAuth
    import pandas as pd
    import requests
    
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

    # make a list to check what for format of nested values
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