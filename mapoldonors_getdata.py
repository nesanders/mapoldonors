"""
Download data on individual campaign contributions (record type 201)
to MA politicians from the OCPF from 2000 (earliest available) through 2019.

The base form is: https://www.ocpf.us/Reports/SearchItems
"""

import pandas as pd
import os

# record type 201 is individual contributions
rec_type = 201
rec_name = 'IndividualContributor'
url = "https://www.ocpf.us/ReportData/GetTextOutput?1=1&searchTypeCategory=A&recordTypeId={}&startDate={}/{}/01&endDate={}/{}/01&filerCpfId=0&sortField=Date&sortDirection=ASC"

for start_year in range(2000, 2019+1):
    for start_month in range(1,12+1):
        if start_month == 12:
            end_year = start_year + 1
            end_month = 1
        else:
            end_year = start_year
            end_month = start_month + 1
        
        fill_url = url.format(
            rec_type,
            start_year,
            str(start_month).zfill(2),
            end_year,
            str(end_month).zfill(2),
            )
        df = pd.read_table(fill_url, delimiter='\t') 
        df.to_csv('OCPF_'+rec_name+'_'+str(start_year)+'_'+str(start_month).zfill(2)+'.csv')

## Compress
for start_year in range(2000, 2019+1):
    os.system('zip OCPF_IndividualContributor_'+str(year) +'_csvs.zip OCPF_IndividualContributor_'+str(year)+'_*.csv')

