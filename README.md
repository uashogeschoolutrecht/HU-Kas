# HU-Kas

In o.a. de Onderwijs- en Examenregeling (OER-HU) en de studiegids zijn de rechten en plichten van de HU-studenten ten aanzien van onderwijs en toetsen geregeld. Wanneer je van mening bent dat er voor jou een uitzondering moet worden gemaakt, of wanneer je van mening bent dat de OER-HU opgevolgd moet worden, kun je een verzoek indienen bij jouw examencommissie via het verzoekensysteem HUKAS. Hierbij kun je denken aan een verzoek om een extra toetskans, vrijstelling, alternatieve toetsvorm of een verzoek om een voorziening in het kader van onbelemmerd studeren.

De examencommissie van het instituut neemt alleen verzoeken in behandeling die worden ingediend via HUKAS.

Metadata of this datasource is available through: <https://hukas.hu.nl/odata/Hukas_OData/v1/$metadata>
An overview of available tables are here:


<pre><code>TABLE: Files
SUB TABLES:
    Behandelaar
    BehandelendePartij
    Cases
    Decisions
    Status
    StatusChanges
 
TABLE: Casess
SUB TABLES:
    File
    RequesterType
 
TABLE: Decisions
SUB TABLES:
    File
    StatusChanges
 
TABLE: Statuss
SUB TABLES:
    Files
    StatusChanges
    StatusChanges_2
 
TABLE: RequesterTypes
SUB TABLES:
    Casess
    StatusChanges
 
TABLE: BehandelendePartijs
SUB TABLES:
    Files
 
TABLE: StatusChanges
SUB TABLES:
    Decision
    File
    Status from
    Status_to
 
TABLE: CustomAccounts
SUB TABLES:
    Files
 </code></pre>
 ## Requirements

- Access to Team D&A Azure Key Vault secret KVK-API-HUKAS-PROD
- Have Az.Accounts module installed and connection between PowerShell and Azure set up

## Summary

This repo consists of 3 Python scripts.

 1. Script functions.py has a the functions needed for this application
 2. Script main.py collects the credentials to access the data, load the data and writes them into csv files.
 3. Script readmeta.py this script returns an overview of all avalaible tables

In more detail the following steps are performed:

- Get credentials to access data tables from Azure Data Vault
- Set up a connection through the HU-Kas ODATA api endpoint
- Get fact table
- Get dimension tables
- Write all tables to csv files
