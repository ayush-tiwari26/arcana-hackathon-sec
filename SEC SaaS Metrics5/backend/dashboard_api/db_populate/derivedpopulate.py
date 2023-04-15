from dashboard_api.models import BaseMetrics, DerivedMetrics
from dashboard_api.models import Companies
import pandas as pd
from django.db.models import Q
import os
import json

BASE=r"dashboard_api\cik_data\master\\"
for file in os.listdir(BASE):
    print(file)
    derived_met_list=pd.read_csv(BASE+file)
    list = []
    for _, row in derived_met_list.iterrows():
        dict_ = {}
        dict_['company'] = Companies.objects.get(cik=str(int(row['cik'])))
        dict_['tag'] = row['metric']
        dict_['value'] = row['value']
        dict_['accession_no'] = row['accession_number']
        dict_['form_type'] =  row['form_type']
        dict_['filing_date'] = None if (len(str(row['filing_date']))<5) else str(row['filing_date'])
        dict_['sentence_date'] = dict_['filing_date']
        dict_['formula'] =  row['formula']
        list.append(DerivedMetrics(**dict_))
    DerivedMetrics.objects.bulk_create(list)
    
    m2m_set = []
    for _, row in derived_met_list.iterrows():
        derived_item = DerivedMetrics.objects.filter(Q(tag = row['metric']) & Q(accession_no=row['accession_number']))[0]
        data = json.loads(row['base_dependencies'])
        for i in range(len(data['tag'])):
            if(data['tag'][i]=='us-gaap:StockholdersEquity'):
                continue
            base_item = BaseMetrics.objects.filter(Q(company__id = derived_item.company.id) & Q(tag = data['tag'][i]) & Q(filing_date=str(data['date'][i].split()[0])))[0]
            m2m_set.append(DerivedMetrics.base_metrics.through(derivedmetrics_id=derived_item.id,basemetrics_id=base_item.id))
    if(len(m2m_set)>0):
        DerivedMetrics.base_metrics.through.objects.bulk_create(m2m_set)
