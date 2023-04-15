from dashboard_api.models import SentimentModel
from dashboard_api.models import Companies
import pandas as pd
from django.db.models import Q
import os
import json

BASE="dashboard_api/cik_data/sentiment/"
failed = []
for file in os.listdir(BASE):
    print(file)
    if(1):
        derived_met_list=pd.read_csv(BASE+file, index_col=0)
        list = []
        for _, row in derived_met_list.iterrows():
            dict_ = {}
            dict_['item'] = row.name
            dict_['company'] = Companies.objects.get(cik=file.split('_')[1])
            if row['confidence'] != "empty" :
                dict_['confidence'] = row['confidence']
            else:
                continue 
            dict_['label'] = row['label']
            # dict_['accession_no'] = file.split('_')[3]
            date = file.split('_')[2]
            dict_['filing_date'] = date[:4]+"-"+date[4:6]+"-"+date[6:]

            pos_neg = row['sentences_highlight'].replace('(', '[').replace(')', ']')
            dict_['positive'] = json.loads(pos_neg.split("'negative': ")[0][13:-2])
            dict_['negative'] = json.loads(pos_neg.split("'negative': ")[1][:-1])
            list.append(SentimentModel(**dict_))
    SentimentModel.objects.bulk_create(list)