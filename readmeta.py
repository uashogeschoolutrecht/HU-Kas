# Script to get more insight into how the meta-data for HU kas looks. 

# Fetch credentials from Key Vault
from functions import getAzureKey

user = getAzureKey('KV-DENA', 'KVK-API-HUKAS-PROD')
ww = getAzureKey('KV-DENA', 'KVW-API-HUKAS-PROD')

# Get meta data on the tables of HU Kas
def getHukasTables(user,ww):
    import pandas as pd
    from requests.auth import HTTPBasicAuth
    import requests

    # Set up HTTP authenticion
    auth = HTTPBasicAuth(user, ww)

    # set base URL for HUKAS
    base_url = 'https://hukas.hu.nl/odata/Hukas_OData/v1/'

    # Set up a connection to HU Kas using above URL and authentication credentials
    r = requests.get(base_url, auth=auth)

    import xmltodict
    # Convert XML to dict (=JSON-like)
    o = xmltodict.parse(r.content)
    # Create dataframe with table names
    table_names = pd.DataFrame(o['service']['workspace']['collection'])['@href']
    tables = list(table_names)

    # Create empty table_dict
    table_dict = {}

    # loop through tables and get subtables (columns)
    for table in tables:

        # Connect to metadata url
        r = requests.get(f'{base_url}$metadata#{table}', auth=auth)

        # If connection request is valid
        if r.status_code == 200:   

            # Get metadata from XML response
            o = xmltodict.parse(r.content)    

            # Extract the navigation towards the data for each table
            temp = pd.DataFrame(
                pd.DataFrame(
                    o['edmx:Edmx']['edmx:DataServices']['Schema'])
                    ['EntityContainer'][0]['EntitySet'])
            temp = pd.json_normalize(
                pd.DataFrame(temp[temp['@Name']==table]
                ['NavigationPropertyBinding'])
                ['NavigationPropertyBinding'])

            # Create empty list
            sub_tables = []

            # if only one subtable then
            try: 
                sub_tables += [temp['@Path'][0]]
            # For multiple subtables
            except:
                for c in temp.columns:    
                    sub_tables += [temp[c][0]['@Path']]
                    
            table_dict.update({table:sub_tables})

    return table_dict

