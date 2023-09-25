# HU-Kas

In o.a. de Onderwijs- en Examenregeling (OER-HU) en de studiegids zijn de rechten en plichten van de HU-studenten ten aanzien van onderwijs en toetsen geregeld. Wanneer je van mening bent dat er voor jou een uitzondering moet worden gemaakt, of wanneer je van mening bent dat de OER-HU opgevolgd moet worden, kun je een verzoek indienen bij jouw examencommissie via het verzoekensysteem HUKAS. Hierbij kun je denken aan een verzoek om een extra toetskans, vrijstelling, alternatieve toetsvorm of een verzoek om een voorziening in het kader van onbelemmerd studeren.

De examencommissie van het instituut neemt alleen verzoeken in behandeling die worden ingediend via HUKAS.

Metadata of this datasource is available through: <https://hukas.hu.nl/odata/Hukas_OData/v1/$metadata>

## Requirements

- Access to Team D&A Azure Key Vault secret KVK-API-HUKAS-PROD
- Have Az.Accounts module installed and connection between PowerShell and Azure set up

## Summary

This repo consists of 2 Python scripts.

 1. Script library.py describes the data tables of which data is imported
 2. Script main.py collects the credentials to access the data, load the data and writes them into csv files.

In more detail the following steps are performed:

- Get credentials to access data tables from Azure Data Vault
- Set up a connection through the HU-Kas ODATA api endpoint
- Get fact table
- Get dimension tables
- Write all tables to csv files
