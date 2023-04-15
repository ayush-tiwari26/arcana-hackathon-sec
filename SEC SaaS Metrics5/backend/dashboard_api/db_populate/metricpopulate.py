from dashboard_api.models import RiskModel
from dashboard_api.models import Companies
import pandas as pd
import os

BASE=r"dashboard_api\cik_data\risk_metric.csv"
failed_files=[]
df_met=pd.read_csv(BASE)
for index, row in df_met.iterrows():
    try:
        obj=RiskModel(company=Companies.objects.get(cik=str(row['CIK'])),filing_date = str(row['year']),financial = row['financial'],otheridiosyncracies= row['other-idiosyncratic'],legal = row['legal and regulatory'],othersystematic= row['other-systematic'] ,tax= row['tax'])
        obj.save()
    except:
        print(row['CIK']+" "+row['year'])
