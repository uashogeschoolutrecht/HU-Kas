from functions import getAzureKey

user = getAzureKey('KV-DENA', 'KVK-API-HUKAS-PROD')
ww = getAzureKey('KV-DENA', 'KVW-API-HUKAS-PROD')

def getHukasTables(user,ww):
    import pandas as pd
    from requests.auth import HTTPBasicAuth
    import requests

    auth = HTTPBasicAuth(user, ww)

    # set base URL for HUKAS
    base_url = 'https://hukas.hu.nl/odata/Hukas_OData/v1/'

    r = requests.get(base_url, auth=auth)

    import xmltodict
    # get metadata from XML
    o = xmltodict.parse(r.content)
    table_names = pd.DataFrame(o['service']['workspace']['collection'])['@href']

    tables = list(table_names)

    # set table_dict
    table_dict = {}

    import xmltodict

    # loop through tables and get subtables
    for table in tables:

        r = requests.get(f'{base_url}$metadata#{table}', auth=auth)

        if r.status_code == 200:   

            o = xmltodict.parse(r.content)    

            temp = pd.DataFrame(
                pd.DataFrame(
                    o['edmx:Edmx']['edmx:DataServices']['Schema'])
                    ['EntityContainer'][0]['EntitySet'])
            temp = pd.json_normalize(
                pd.DataFrame(temp[temp['@Name']==table]
                ['NavigationPropertyBinding'])
                ['NavigationPropertyBinding'])

            sub_tables = []

            # if only one subtable then
            try: 
                sub_tables += [temp['@Path'][0]]
            except:
                for c in temp.columns:    
                    sub_tables += [temp[c][0]['@Path']]
                    
            table_dict.update({table:sub_tables})

    return table_dict

