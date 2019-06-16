"""
Summarize OCPF individual campaign contributions data from 2000 to 2013
to politicians in the Mystic River watershed of MA.

The base OCPF form the data is from is: https://www.ocpf.us/Reports/SearchItems

Usage: python3 mapoldonors_summarize.py [ini_config_file]

ini_config_file defaults to 'default.ini', which provides an example of the form and content of that script

The InFilename in the config file defaults to 'OCPF_IndividualContributor.zip', the output of the mapoldonors_getdata.py script
"""

import pandas as pd
from configparser import SafeConfigParser
import io, sys, ast
from zipfile import ZipFile
from datetime import datetime

combine_name = lambda x: x['Name'] + (', ' + x['First Name'] if len(x['First Name'])>0 else '')

## Identify config file
if len(sys.argv)>1 and sys.argv[1].endswith('.ini'):
    config_file = sys.argv[1]
else:
    config_file = 'default.ini'

## Parse the ini
config = SafeConfigParser()
config.read(config_file)
## Load filter rules
filter_set = {}
filter_cols = ['DonorNameReverse', 'City', 'State', 'Occupation', 'Employer', 'FilerFullNameReverse']
for col in filter_cols:
    filter_set[col] = ast.literal_eval(config['filters'][col])
if ast.literal_eval(config['filters']['DateRange']) is None:
    filter_date = None
else:
    filter_date = [pd.to_datetime(c) for c in ast.literal_eval(config['filters']['DateRange'])]
group_list = ast.literal_eval(config['format']['GroupList'])
top_N = int(config['format']['TopN'])
out_filename = config['IO']['OutFilename']
data_file = config['IO']['InFilename']

## Load data files
zf = ZipFile(data_file)
dfs = {}
for cf in zf.namelist():
    ## Read csv in zip
    df = pd.read_csv(zf.open(cf), lineterminator='\n')
    if len(df) > 1:
        ## Transform key columns
        df.rename({'Filer Full Name Reverse':'FilerFullNameReverse'}, axis='columns', inplace=True)
        for col in ['Name', 'First Name', 'Address', 'City', 'State', 'Occupation', 'Employer','FilerFullNameReverse']:
            df[col] = df[col].fillna('').str.upper()
        df['DonorNameReverse'] = df.apply(combine_name, axis=1)
        ## Apply string filters
        for col in filter_cols:
            if filter_set[col] is not None:
                df = df[df[col].isin(filter_set[col])]
        ## Apply date filters
        df['Date'] = pd.to_datetime(df['Date'])
        if filter_date is not None:
            df = df[(df['Date'] >= filter_date[0]) & (df['Date'] <= filter_date[1])]
        ## Output
        dfs[cf] = df

## Concatenate all monthly files
all_df = pd.concat(dfs).reset_index()

## Format output
form_df = all_df.groupby(group_list).apply(lambda x: x.groupby('DonorNameReverse')[['Amount']].sum().nlargest(top_N, columns='Amount'))
sel_name = form_df.index.get_level_values(form_df.index.names.index('DonorNameReverse')).values
for col in ['Address', 'City', 'State', 'Occupation', 'Employer']:
    if col not in group_list:
        form_df[col] = all_df.groupby('DonorNameReverse')[col].last().loc[sel_name].values

form_df.sort_values(ascending = False, by = group_list+['Amount']).to_csv(out_filename)
