from dashboard_api.models import BaseMetrics
from dashboard_api.models import Companies
import pandas as pd
import os

BASE_METRIC = r"dashboard_api\cik_data\xbrl-2021-10k10q.csv"
BASE=r"dashboard_api\cik_data\base\base_met_master\\"
failed_files=[]
for file in os.listdir(BASE):
    print(file)
    base_met_list=pd.read_csv(BASE+file)
    base_mey_list=base_met_list.reset_index(drop=True)
    try:
        BaseMetrics.objects.bulk_create([BaseMetrics(**{
                                    'company' : Companies.objects.get(cik=str(row['CIK'])),
                                    'tag' : row['xbrl_tag_name'],
                                    'value' : row['value'],
                                    'unit' : row['unitref'],
                                    'accession_no' : row['accession_no'],
                                    'filing_date': None if (len(str(row['FilingDate']))<5) else str(row['FilingDate']) ,
                                    'form_type': row['FormType'],
                                    'source': row['source']})
                        for _,row in base_met_list.iterrows()])
    except:
        print("failed")
        failed_files.append(file)
print(failed_files)
    

    # bmlist=base_met_list['Metric name'].tolist()
    # print(bmlist)
    # print(len(base_metric))
    # continue
    # for index,row in base_metric.iterrows():
    #     company_cik = str(row['CIK']).lstrip("0") 
    #     company1=Companies.objects.get(cik=company_cik)
    #     tag1 = row['xbrl_tag_name']
    #     value1 = row['value']
    #     unit1 = row['unitref']
    #     accession_no1 =row['accession_no']
        
    #     if(len(str(row['FilingDate'])) >5):
    #         filing_date1 = str(row['FilingDate'])
    #     else:
    #         filing_date1 = None

    #     form_type1 = row['FormType']
    #     # print(type(start_date1))
    #     # if tag1 in bmlist:
    #         # print('save')
    #     obj=BaseMetrics( company = company1,tag = tag1,value = value1,unit =unit1,accession_no = accession_no1,filing_date=filing_date1,form_type=form_type1)
    #     obj.save()
    