import requests
import json
import time
from bs4 import BeautifulSoup 
import pandas as pd
c=0
base=r"C:\Users\Goutam Chakraborty\web_env\sec-dashboard-backend\dashboard_api\cik_data\htmldata\\"
def balance_sheet(cik,c):
    print('xxxxxxxxxxxxxxxxxxxxxxxxx')
    print(c)
    
    print(cik)
    headers= {'User-Agent': 'E-cellankit.bagde2000@ecell-iitkgp.org'}
    start_yr=2017
    end_yr=2022
    forms = ['10-K']
    print("---------------------")
    cik_no = str(cik)
    cik_no = cik_no.zfill(10)
    submission_url = "https://data.sec.gov/submissions/CIK{}.json".format(cik_no)
    content = requests.get(submission_url, headers=headers)
    print(content)
    content = content.json()
    accession_dict = {}
    filingDate=[]
    formtype=[]
    for x in range(len(content['filings']['recent']['accessionNumber'])):
        if(content['filings']['recent']['form'][x] in forms):
            accession_dict[content['filings']['recent']['accessionNumber'][x]] = content['filings']['recent']['form'][x] 
            filingDate.append(content['filings']['recent']['filingDate'][x])
            formtype.append(content['filings']['recent']['form'][x])
  
    accession_nos=[]
    filingdate2=[]
    formtype2=[]
    c=0
    for key in accession_dict.keys():
        accession_no = key
        tempn=key
        tempn=tempn.split('-')
        yr=tempn[1]

        if int(yr)+2000>=int(start_yr) and int(yr)+2000<=int(end_yr) :
            accession_nos.append(key)
            filingdate2.append(filingDate[c])
            formtype2.append(formtype[c])
        c+=1
    fin_data=[]
    count=0
    for accession_no in accession_nos:
        base_url = r"https://www.sec.gov"
        normal_url = r"https://www.sec.gov/Archives/edgar/data/"+cik_no+"/"+accession_no+"/index.json"
        normal_url = normal_url.replace('-','')
        print(normal_url)
        content = requests.get(normal_url, headers=headers)
        print(content)
        content=content.json()
        year=str(filingdate2[count]).split('-')[0]
        count+=1
        for file in content['directory']['item']:
    
            # Grab the filing summary and create a new url leading to the file so we can download it.
            if file['name'] == 'FilingSummary.xml':

                xml_summary = base_url + content['directory']['name'] + "/" + file['name']
        
                print('-' * 100)
                print('File Name: ' + file['name'])
                print('File Path: ' + xml_summary)  

                base_url = xml_summary.replace('FilingSummary.xml', '')

        # request and parse the content
        content = requests.get(xml_summary, headers=headers).content
        soup = BeautifulSoup(content, 'lxml')

        # find the 'myreports' tag because this contains all the individual reports submitted.
        reports = soup.find('myreports')
        time.sleep(2)
        # I want a list to store all the individual components of the report, so create the master list.
        master_reports = []

        # loop through each report in the 'myreports' tag but avoid the last one as this will cause an error.
        reporttemp={}
        reporttemp['year']=year
        for report in reports.find_all('report')[:-1]:

            # let's create a dictionary to store all the different parts we need.
            report_dict = {}
            report_dict['name_short'] = report.shortname.text
            report_dict['name_long'] = report.longname.text
            report_dict['position'] = report.position.text
            report_dict['category'] = report.menucategory.text
            report_dict['url'] = base_url + report.htmlfilename.text

            # append the dictionary to the master list.
            master_reports.append(report_dict)

        statements_url = []
        statementsname=[]
        for report_dict in master_reports:
    
            # define the statements we want to look for.
            item1 = r"balance sheets"
            item2 = r"statements of income"
            item3 = r"statements of cash flows"
            
            
    
            # store them in a list.
            report_list = [item1, item2, item3]

            # if the short name can be found in the report list.
            if (item1 in report_dict['name_short'].lower()) or (item2 in report_dict['name_short'].lower()) or (item3 in report_dict['name_short'].lower()) :
                
                # print some info and store it in the statements url.
                print('-'*100)
                print(report_dict['name_short'])
                print(report_dict['url'])
        
                statements_url.append(report_dict['url'])
                statementsname.append(report_dict['name_short'] )

        
        k=0
        yr_data=[]
        for url in statements_url:
            print(url)
            #print(url)
            
            headers2 = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            content = requests.get(url, headers=headers).content
            print(content)
            report_soup = BeautifulSoup(content, 'html')
            data=report_soup.findAll('table')[0]
            #print(data)
            data_list={}
            for a in data.findAll('a'):
                a.replaceWithChildren()
            for e in data.findAll('br'):
                e.replace_with('')
            for tag in data():
                for attribute in ["style"]:
                    del tag[attribute]
            data2 = data.find('table',{"class": "outerFootnotes"})
            if data2 is not None :
                data2.replaceWith('')
            #data=div_bs4
            print(data)
            data_list['tablename']=statementsname[k]
            data_list['table_data']=(str(data))
            k+=1
            yr_data.append(data_list)
        reporttemp['data']=yr_data
        fin_data.append(reporttemp)
    with open(base+'data'+str(cik)+'.json', 'w') as fp:
        json.dump(fin_data, fp)

df=pd.read_csv(r'dashboard_api\cik_data\cik_sheet.csv')
cikn=df['CIK Number'].tolist()
cikn=['78749']
done=[]
for i in range (len(cikn)):

    done.append(cikn)
    c+=1
    balance_sheet(cikn[i],c)
    