from dashboard_api.models import Companies
import pandas as pd
import requests
CSV_FILE_CIKS = r"dashboard_api\cik_data\cik_sheet.csv"
print("ok")
headers = {'User-Agent': 'Mozilla'}
cik_name = pd.read_csv(CSV_FILE_CIKS)
print(len(cik_name))
for i in range(len(cik_name)):
    print("ok")
    cik_no = cik_name['CIK Number'][i]
    cik_no = cik_name['CIK Number'][i]
    cik_no = str(cik_no)
    cik_no = cik_no.zfill(10)
  
    print("Parsing company {}, cik number: {}".format(cik_name['Company'][i], cik_no))
  
    company = cik_name['Company'][i]

    ## get submission file
    submission_url = "https://data.sec.gov/submissions/CIK{}.json".format(cik_no)
    print("submission url : {}".format(submission_url))

    # request the url and decode it.
    content = requests.get(submission_url, headers=headers)
    content = content.json()
    cik1=content['cik']
    name1=content['name']
    ticker1=content['tickers']
    website1=content['website']
    address1=content['addresses']
    if(content['phone']):
        phone1=content['phone']
    else:
        phone1=""

    
    sic1=content['sic']
    category1=content['category']
    stateOfIncorporation1=content['stateOfIncorporation']


    obj=Companies( cik = cik1,name = name1,ticker = ticker1,website = website1,addresses =address1,phone = phone1,sic=sic1,category=category1,state_of_incorporation=stateOfIncorporation1)
    obj.save()
  
