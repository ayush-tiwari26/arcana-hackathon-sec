from dashboard_api.models import Companies
import pandas as pd
import requests
CSV_FILE_CIKS = r"C:\Users\Goutam Chakraborty\web_env\sec-dashboard-backend\dashboard_api\cik_data\InterIIT DigAlpha - OVERVIEW.csv"
print("ok")
headers = {'User-Agent': 'Mozilla'}
df=pd.read_csv(CSV_FILE_CIKS)
for index,row in df.iterrows():
    print(row['CIK Number'])
    try:
        b = Companies.objects.get(cik=int(row['CIK Number']))
        b.overview=row['OVERVIEW']
        yr=(str(row['YEAR']))
        yr=yr.split('.')[0]
        b.founding_year=yr
        b.save()
    except:
        yr=(str(row['YEAR']))
        yr=yr.split('.')[0]
        b=Companies(cik =row['CIK Number'] ,name = row['Company'],founding_year=yr,overview=row['OVERVIEW'])
        b.save()
        print("no")