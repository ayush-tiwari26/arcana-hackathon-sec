from dashboard_api.models import BaseMetrics, DerivedMetrics
from dashboard_api.models import Companies
import pandas as pd
from django.db.models import Q
import os
import json

BASE="dashboard_api/cik_data/roberta-year/"
failed = []
for file in os.listdir(BASE):
    print(file)
    if(1):
        derived_met_list=pd.read_csv(BASE+file)
        list = []
        for _, row in derived_met_list.iterrows():
            dict_ = {}
            dict_['company'] = Companies.objects.get(cik=file.split('_')[1])
            dict_['tag'] = row['metric']
            dict_['value'] = float(row['number'])
            dict_['accession_no'] = file.split('_')[3]
            dict_['form_type'] =  "10-K"
            date = file.split('_')[2]
            # dict_['filing_date'] = None if (len(str(row['filing_date']))<5) else date[:4]+"-"+date[4:6]+"-"+date[6:]
            dict_['filing_date'] = str(row['year'])+"-12-31"
            dict_['sentence_date'] = row['date']
            dict_['score'] =  row['score']
            dict_['sentence'] =  row['sentence']
            dict_['source'] =  'text'
            list.append(DerivedMetrics(**dict_))
        os.remove(BASE+file)
        DerivedMetrics.objects.bulk_create(list)
        print("success")
    # except:
    #     failed.append(file)