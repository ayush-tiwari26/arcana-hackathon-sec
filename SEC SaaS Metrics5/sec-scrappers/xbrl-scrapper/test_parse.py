
import numpy as np
import requests 
import os
import json
import pandas as pd
import requests
import zipfile
import datetime
from zipfile import ZipFile
import glob
from pysecxbrl.parsing import SECParser
from pysecxbrl.extract import XBRLExtractor
import psycopg2
from datetime import date
import boto3

CSV_FILE_CIKS = os.path.expanduser("~/sec-scraper/data/input_data/cik_sheet.csv")
BASE_FOLDER = os.path.expanduser("~/sec-scraper/data/")
DAILY_MASTER_CSV_PATH =  BASE_FOLDER + "parsed_data/xbrl/master-{}.csv".format(date.today())
folder = BASE_FOLDER+"temp2"

# for base metrics extraction
UNIVERSAL_MASTER_CSV_PATH = os.path.expanduser('~/sec-scraper/data/parsed_data/xbrl/master2017-22_new.csv')

BASE_METRICS_LIST_PATH = os.path.expanduser('~/sec-scraper/data/input_data/base_metrics_list.csv')
MODIFIED_METRICS_BASEPATH = os.path.expanduser('~/sec-scraper/data/parsed_data/xbrl/{}/'.format(date.today()))

SNS_ARN = 'arn:aws:sns:ap-south-1:144883820914:secScraperTopic'
links = []

headers = {'User-Agent': 'E-cell ankit.bagde@ecell-iitkgp.org'}
forms = ['10-K', '10-Q']
start_yr='2021'
end_yr='2022'
# create folder to store zip file
if not os.path.exists(os.path.expanduser(folder)):
    os.makedirs(os.path.expanduser(folder))

################################
# DO NOT MODIFY BELOW
###############################

df_list = []
parser = SECParser()
extractor = XBRLExtractor()
cik_name = pd.read_csv(CSV_FILE_CIKS)

SUCCESSFUL_CIKS = []
FAILED_CIKS = []
NOT_PRESENT_CIKS =[]
YR_FAILED=[0,0,0,0,0,0]
YR_SUCCESS=[0,0,0,0,0,0]
YR_NOTPRESENT=[0,0,0,0,0,0]

###################################
# Connect to DB to check if filing is in DB
###################################
connection = psycopg2.connect(
    host = 'database-1.cpf4sdgr78cy.us-east-2.rds.amazonaws.com',
    port = 5432,
    user = 'postgres',
    password = 'saasifi-t5',
    database='edgardb'
    )

cursor=connection.cursor()

print("PostgreSQL server information")
print(connection.get_dsn_parameters(), "\n")


###################################
# Checks whether filing with given accession number is in DB
###################################

def checkFilingExists(accession_no):

    global cursor
    query = """SELECT * FROM dashboard_api_basemetrics WHERE accession_no='{}'""".format(accession_no)

    cursor.execute(query)
    record = cursor.fetchall()

    if(len(record) == 0):
        return False
    return True

##################################################
# Creates base metrics csv files for each company
##################################################

def createBaseMetrics(df1):

    base=pd.read_csv(BASE_METRICS_LIST_PATH)
    basemet=base['Metric name'].tolist()
    df1 = df1[df1.xbrl_tag_name.isin(basemet)]

    ls_index=[]
    df_filtered=df1.dropna(axis=0, subset=['value'])
    for index,row in df_filtered.iterrows():
        row['value']=row['value'].replace(',','')
        try:
            row['value']=float(row['value'])
        except:
            ls_index.append(index)

    df_filtered=df_filtered.drop(ls_index,axis=0)
    df2=df_filtered

    df2['accession_no'].isnull().values.any()
    y=df2.groupby(['xbrl_tag_name'])

    print(y.groups.keys())
    k=0
    try:
        grp=y.get_group('us-gaap:CostOfGoodsAndServicesSold')

        y=grp.groupby(['CIK','accession_no','xbrl_tag_name','unitref','FilingDate','FormType'])['value'].sum()
        df_final2=y.reset_index(name = 'value')
    except:
        k=1 

    x=df_filtered.groupby(['CIK','accession_no','xbrl_tag_name','unitref','FilingDate','FormType'])['value'].max()
    df_final=x.reset_index(name = 'value')
    index_names = df_final[ df_final['xbrl_tag_name']=='us-gaap:CostOfGoodsAndServicesSold'].index

    df_final.drop(index_names, inplace = True)
    if(k==0):
        df_final.append(df_final2)
      
    if(df_final.empty == False):
        with open(UNIVERSAL_MASTER_CSV_PATH, 'a') as f:
            x = df_final.to_string(header=False,
                  index=False,
                  index_names=False).split('\n')
            vals = [','.join(ele.split()) for ele in x]

            for line in vals:
                f.write(line + '\n')



    x=df_final.groupby(['CIK'])
    list_cik=list(x.groups.keys())
    for k in list_cik:
        df=x.get_group(k)
        df = df.astype({"CIK": int})
        df = df.assign(source='xbrl')
        if(df.empty == False):
            df.to_csv(MODIFIED_METRICS_BASEPATH + str(k) + '.csv')




def extractor(accession_nos,i,cik_name,cik_no,filingDate,formtype):
    parser = SECParser()
    extractor = XBRLExtractor()
    count=0
    for accession_no in accession_nos:
        parser = SECParser()
        extractor = XBRLExtractor()
        accn = accession_no.replace('-','')
        cn = cik_no.lstrip('0')
        fildate=filingDate[count]
        formType=formtype[count]
        count+=1
        
  
        file_url = "https://www.sec.gov/Archives/edgar/data/"+cn+"/"+accn+"/"+accession_no+"-xbrl.zip"
        os.system("""wget -q --user-agent "Mozilla/5.0"   -O "data.zip" {}""".format(file_url) )
        try:
            with zipfile.ZipFile("./data.zip",'r') as zipObj:
                zipObj.extractall(folder)
        except:
            print("FAILED2\n\n")
            FAILED_CIKS.append((cik_name['Company'][i], cik_no))
            return

        # extract tags in json format
        try:
            files = extractor.identifyFiles(folder)
            main_data_f = files["main"][0]
            calc_f = files["calculation"][0]

            with open(os.path.join(folder, calc_f)) as f:
                txt_calc = f.read()
                calc_elems = parser.parseCalculationXML(txt_calc)

            with open(os.path.join(folder, main_data_f)) as f:
                txt = f.read()
                ctx_elems, data_elems  = parser.parseMainXBRL(txt)

            df = pd.DataFrame()
            value = []
            name = []
            acc_no=[]
            contexref = []
            decimals = []
            startdate = []
            enddate = []
            identifier = []
            data1 = []
            scale = []
            xbrl_tag = []
            xbrl_prefix = []
            instant = []
            segment = []
            unitref= []
            explicitmember = []
            dimension = []
            period = []
            tagname=[]
            filing_date=[]
            form_type=[]
            for key2 in data_elems.keys():
                value.append(data_elems[key2]['value'])
                contexref.append(data_elems[key2]['contextRef'])
                acc_no.append(accession_no)
                filing_date.append(fildate)
                form_type.append(formType)
                #print(contexref)
                tag=""
                name=""
                # to handle 2 types of json
                if 'name' in data_elems[key2].keys() and len(data_elems[key2]['name'].split(':'))==2:
                    xbrl_tag.append(data_elems[key2]['name'].split(':')[1])
                    xbrl_prefix.append(data_elems[key2]['name'].split(':')[0]) 
                    tag= data_elems[key2]['name'].split(':')[1]
                    name= data_elems[key2]['name'].split(':')[0] 
                    try:
                        if('decimals' in data_elems[key2]):
                            value[-1] = str(float(value[-1].replace(',',''))*pow(10,-int(data_elems[key2]['decimals'])))
                    except:
                        pass
                elif 'tag' in data_elems[key2].keys():
                    xbrl_tag.append(data_elems[key2]['tag'])
                    xbrl_prefix.append(data_elems[key2]['prefix']) 
                    tag=data_elems[key2]['tag']
                    name= data_elems[key2]['prefix']      
                else:
                    xbrl_tag.append(None)
                    xbrl_prefix.append(None)
                if tag!="" and name!="":
                    tagname.append(name+":"+tag)
                elif tag!="":
                    tagname.append(tag)
                elif name!="":
                    tagname.append(name)
                else:
                    tagname.append(None)

                if 'decimals' in data_elems[key2].keys():
                    decimals.append(data_elems[key2]['decimals'])
                else:
                    decimals.append(None)

                if 'scale' in data_elems[key2].keys():
                    scale.append(data_elems[key2]['scale'])
                else:
                    scale.append(None)

                if 'unitRef' in data_elems[key2].keys():
                    unitref.append(data_elems[key2]['unitRef'])
                else:
                    unitref.append(None)

                if 'startDate' in ctx_elems[contexref[-1]].keys():
                    startdate.append(ctx_elems[contexref[-1]]['startDate'])
                else: 
                    startdate.append(None)

                if 'endDate' in ctx_elems[contexref[-1]].keys():
                    enddate.append(ctx_elems[contexref[-1]]['endDate'])
                else: 
                    enddate.append(None)

                if(startdate[-1] is not None and enddate[-1] is not None):
                    if(datetime.datetime.strptime(enddate[-1], "%Y-%m-%d") - datetime.datetime.strptime(startdate[-1], "%Y-%m-%d") < datetime.timedelta(days=120)):
                        period.append("quarterly")
                    else:
                        period.append("yearly")
                else:
                    period.append(None)

                if 'instant' in ctx_elems[contexref[-1]].keys():
                    instant.append(ctx_elems[contexref[-1]]['instant'])
                else: 
                    instant.append(None)

                if 'segment' in ctx_elems[contexref[-1]].keys() and len(ctx_elems[contexref[-1]]['segment'])>0:
                    if 'explicitMember' in ctx_elems[contexref[-1]]['segment'][0].keys():
                        explicitmember.append(ctx_elems[contexref[-1]]['segment'][0]['explicitMember'])
                    else:
                        explicitmember.append(None)
                else: 
                    explicitmember.append(None)

                if 'segment' in ctx_elems[contexref[-1]].keys() and len(ctx_elems[contexref[-1]]['segment'])>0:
                    if 'dimension' in ctx_elems[contexref[-1]]['segment'][0].keys():
                        dimension.append(ctx_elems[contexref[-1]]['segment'][0]['dimension'])
                    else:
                        dimension.append(None)
                else: 
                    dimension.append(None)
                identifier.append(ctx_elems[contexref[-1]]['identifier'])        
    
            df['contexref'] = contexref
            df['value'] = value
            df['decimals'] = decimals
            df['unitref']=unitref
            df['scale']=scale
            df['xbrl_tag']=xbrl_tag
            df['xbrl_prefix']=xbrl_prefix
            df['xbrl_tag_name']=tagname
            df['startdate'] =startdate
            df['enddate'] = enddate
            df['period'] = period
            df['instant']=instant
            df['explicitmember']=explicitmember
            df['dimension']=dimension
            df['accession_no']=acc_no
            df['CIK'] = identifier
            df['FilingDate']=filing_date
            df['FormType']=form_type
            print("xxxxxxx")
            print(identifier[0])
            #path = os.path.join(location, dir)        

            df_list.append(df)
            print("SUCCESSFUL\n\n")
            SUCCESSFUL_CIKS.append((cik_name['Company'][i], cik_no))

        except:
            FAILED_CIKS.append((cik_name['Company'][i], cik_no))
            
            
        finally:
            for f in os.listdir(folder):
                os.remove(os.path.join(folder, f))


for i in range(len(cik_name)):
    
    cik_no = cik_name['CIK Number'][i]
    cik_no = cik_name['CIK Number'][i]
    cik_no = str(cik_no)
    cik_no = cik_no.zfill(10)
  
    print("\n\n------------------Parsing company {}, cik number: {}------------------".format(cik_name['Company'][i], cik_no))
  
    company = cik_name['Company'][i]

    ## get submission file
    submission_url = "https://data.sec.gov/submissions/CIK{}.json".format(cik_no)
    print("submission url : {}".format(submission_url))

    # request the url and decode it.
    content = requests.get(submission_url, headers=headers)
    content = content.json()

    accession_dict = {}
    filingDate=[]
    formtype=[]
    fileName = []
    for x in range(len(content['filings']['recent']['accessionNumber'])):
        if(content['filings']['recent']['form'][x] in forms):
            accession_dict[content['filings']['recent']['accessionNumber'][x]] = content['filings']['recent']['form'][x] 
            filingDate.append(content['filings']['recent']['filingDate'][x])
            formtype.append(content['filings']['recent']['form'][x])
            fileName.append(content['filings']['recent']['primaryDocument'][x])


    accession_nos=[]
    filingdate2=[]
    formtype2=[]
    filename2 = []
    
    c=0
    for key in accession_dict.keys():
        accession_no = key
        tempn=key
        tempn=tempn.split('-')
        yr=tempn[1]

        if(int(yr)+2000>=int(start_yr)):
            if(checkFilingExists(accession_no) == False):
                print("accession_no: {} not in DB, adding to list...".format(accession_no))
                accession_nos.append(accession_no)
                filingdate2.append(filingDate[c])
                formtype2.append(formtype[c])
                filename2.append(fileName[c])
                link = "https://www.sec.gov/Archives/edgar/data/{}/{}/{}".format(cik_no.lstrip('0'),accession_no.replace('-',''),fileName[c])
                links.append(link)

            else:
                print("FOUND accession_no: {} in DB".format(accession_no))
        c+=1


    if(len(accession_nos)==0):
        print("\nNo new unprocessed accession_no found")
        NOT_PRESENT_CIKS.append((cik_name['Company'][i], cik_no))
    else:
        extractor(accession_nos,i,cik_name,cik_no,filingdate2,formtype2)


if(len(links)!=0):
    client = boto3.client('sns')
    msg = 'SaaSiFi found the following new filings during daily scraping\n{}'.format("\n".join(item for item in links))
    response = client.publish(
    TargetArn=SNS_ARN,
    Message= msg
    )
else: 
    print("SaaSiFi could not find any new filings")

    client = boto3.client('sns')
    msg = 'SaaSiFi found no new filings during daily scraping\n'
    response = client.publish(
    TargetArn=SNS_ARN,
    Message= msg
    )



flag = False

for _df in df_list:
    if(df.empty == False):
        flag = True
        break

if(flag):
    df_all = pd.concat(df_list, ignore_index = True)
    df_all.to_csv(DAILY_MASTER_CSV_PATH)
    print("INFO: Extracting base metrics from the file")
    createBaseMetrics(df_all)
else:
    pd.DataFrame().to_csv(DAILY_MASTER_CSV_PATH)

print("Created {} file".format(DAILY_MASTER_CSV_PATH.split('/')[-1]))
print(len(SUCCESSFUL_CIKS))
print(len(FAILED_CIKS))
print(len(NOT_PRESENT_CIKS))
