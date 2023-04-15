from ast import Try
from email.mime import base
import json
import datetime
from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
import requests
import time
from bs4 import BeautifulSoup 
from dashboard_api.models import Companies, DerivedMetrics, BaseMetrics,RiskModel
from dashboard_api.serializers import CompaniesSerializer, DerivedMetricsSerializer, BaseMetricsSerializer
from rest_framework.decorators import api_view
import os
from yahoo_fin.stock_info import get_data
import yahoo_fin.stock_info as si
from dashboard_api.models import BaseMetrics, DerivedMetrics,RiskModel, SentimentModel
from dashboard_api.models import Companies
import pandas as pd
from django.db.models import Q
import pandas as pd
from datetime import datetime
now = datetime.now()
import yfinance as yf
from django.views.decorators.cache import cache_page
import boto3

base = "dashboard_api/cik_data/heatmap/"
basehtml = r"dashboard_api/cik_data/htmldata/"
derived=r""

SNS_ARN = 'arn:aws:sns:ap-south-1:144883820914:secScraperTopic'


## API to get all company names and corresponding CIK
@cache_page(60 * 60*2)
@api_view(['GET'])
def companies_list(request):
    if request.method == 'GET':
        try:
            companies = list(Companies.objects.values_list('name', 'cik'))
            companies = {x[0]:x[1] for x in companies}
            return JsonResponse(companies, safe=False)
        except:
            return JsonResponse({}, status=status.HTTP_400_BAD_REQUEST)

## API to fetch company details given it's CIK
@cache_page(60 * 60*2)
@api_view(['GET', 'POST'])
def company_details(request):
    if request.method == 'GET':
        company = Companies.objects.all().filter(cik=str(request.GET['cik']))
        company = CompaniesSerializer(company, many=True)
        return JsonResponse(company.data, safe=False)

    elif request.method == 'POST':
        serializer = CompaniesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

## API to fetch all derived metrics of a particular company over last 5 years
@cache_page(60 * 60*2)
@api_view(['GET'])
def derived_metrics_list(request):
    try:
        if request.method == 'GET':
            ciks = request.GET['cik'].split(',')
            json_ = []
            # for cik in ciks:
            #     if(os.path.exists("dashboard_api/cik_data/derived_metrics/"+cik+".json")):
            #         json_.extend(json.load(open("dashboard_api/cik_data/derived_metrics/"+cik+".json")))
            # return JsonResponse(json_, safe=False)
            
            derived_metrics = DerivedMetrics.objects.all().filter(company__cik__in=list(ciks))
            if("tag" in request.GET):
                derived_metrics = derived_metrics.filter(tag=str(request.GET['tag']))
            if("form_type" in request.GET):
                derived_metrics = derived_metrics.filter(form_type=str(request.GET['form_type']))
            if("start_date" in request.GET):
                date = str(request.GET['start_date']).split('-')
                derived_metrics = derived_metrics.filter(filing_date__gte=datetime.date(int(date[2]), int(date[1]), int(date[0])))
            if("end_date" in request.GET):
                date = str(request.GET['start_date']).split('-')
                derived_metrics = derived_metrics.filter(filing_date__lte=datetime.date(int(date[2]), int(date[1]), int(date[0])))
            metrics_serializer = DerivedMetricsSerializer(derived_metrics.order_by('tag', '-filing_date'), many=True)
            return JsonResponse(metrics_serializer.data, safe=False)
    except:
        return JsonResponse({}, status=status.HTTP_400_BAD_REQUEST)

## API to fetch all base metrics of a particular company over last 5 years
@cache_page(60 * 60*2)
@api_view(['GET','PUT','POST'])
def base_metrics_list(request):
    if request.method == 'GET':
        base_metrics = BaseMetrics.objects.all().filter(company__cik=str(request.GET['cik']))
        if("tag" in request.GET):
            base_metrics = base_metrics.filter(tag=str(request.GET['tag']))
        if("form_type" in request.GET):
            base_metrics = base_metrics.filter(form_type=str(request.GET['form_type']))
        base_metrics_serializer = BaseMetricsSerializer(base_metrics.order_by('filing_date'), many=True)
        return JsonResponse(base_metrics_serializer.data, safe=False)

    elif request.method == 'POST':
        data = request.data
        data['company'] = Companies.objects.get(cik=data['company'])
        try:
            obj = BaseMetrics.objects.create(**data)
            return JsonResponse(BaseMetricsSerializer(obj).data, status=status.HTTP_201_CREATED)
        except:
            return JsonResponse({}, status=status.HTTP_400_BAD_REQUEST)

## API to fetch stock price history from yahoo finance and calculate EV metrics
@cache_page(60 * 60*2)
@api_view(['GET'])
def yahoo_finance(request):
    try:
        if request.method == 'GET':
            start_date="12/04/1910"
            ticker=str(request.GET['cik'])
            today = now.strftime("%Y/%m/%d")
            ticker=Companies.objects.filter(Q(cik = ticker) )[0].ticker
            ticker2=ticker
            ticker=ticker.split(',')
            ticker=ticker[0].strip('[]')[1:-1]
            company={"tag":[], "value":[],"prevpresent":[],"prevvalue":[]}
            data= get_data(ticker, start_date=start_date, end_date=today, index_as_date = True)
            current_price=data.iloc[-1]['close']
            multiple_on_end_firstday=current_price/data.iloc[0]['close']
            multiple_on_ipo_price=current_price/data.iloc[0]['close']

            company['tag'].append('Multiple on IPO Price')
            company['value'].append(multiple_on_ipo_price)
            company['prevpresent'].append(1)
            company['prevvalue'].append(data.iloc[-2]['close']/data.iloc[0]['close'])
            
            quote_table = si.get_quote_table(ticker, dict_result=True)
            company['tag'].append('Share price')
            company['value'].append(current_price)
            company['prevpresent'].append(1)
            company['prevvalue'].append(data.iloc[-2]['close'])
            percent_52_week_high=current_price/float((quote_table['52 Week Range'].split('-')[1]))
            company['tag'].append('Percent of 52 week high')
            company['value'].append(percent_52_week_high)
            company['prevpresent'].append(0)
            company['prevvalue'].append("")

            market_cap=quote_table['Market Cap']
            try:
                d = {'K': 1000, 'M': 1000000, 'B': 1000000000}
                market_cap=float(market_cap[:-1]) *d[market_cap[-1]]
            except:
                market_cap=0

            company['tag'].append('Market Cap')
            company['value'].append(market_cap)
            company['prevpresent'].append(0)
            company['prevvalue'].append("")
            
            k=0
            total_cash =DerivedMetrics.objects.filter(Q(company__ticker = ticker2) & Q(tag = 'Total Cash') & Q(form_type='10-K')).order_by('-filing_date')
            total_debt =DerivedMetrics.objects.filter(Q(company__ticker = ticker2) & Q(tag = 'Total Debt') & Q(form_type='10-K')).order_by('-filing_date')
            if(len(total_cash)>0 and len(total_debt)>0 and total_cash[0].filing_date==total_debt[0].filing_date):
                ev=market_cap+total_cash[0].value+total_debt[0].value
                company['tag'].append('EV')
                company['value'].append(ev)
                if(len(total_cash)>=2 and len(total_debt)>=2 and total_cash[1].filing_date==total_debt[1].filing_date):
                    evprev=market_cap+total_cash[1].value+total_debt[1].value
                    company['prevpresent'].append(1)
                    company['prevvalue'].append(evprev)
                    
                else:
                    company['prevpresent'].append(0)
                    company['prevvalue'].append("")
            else:
                k=1
                company['tag'].append('EV')
                company['value'].append("")
                company['prevpresent'].append(0)
                company['prevvalue'].append("")

            if(k==0):
                try:
                    ltm =DerivedMetrics.objects.filter(Q(company__ticker = ticker2) & Q(tag = 'LTM Revenue') & Q(form_type='10-K')).order_by('-filing_date')
                    evltm=ev/ltm[0].value
                    company['tag'].append('EV/LTM Revenue')
                    company['value'].append(evltm)
                    if (len(ltm)>=2):
                        company['prevpresent'].append(1)
                        evltm=evprev/ltm[1].value
                        company['prevvalue'].append(evltm)
                    else:
                        company['prevpresent'].append(0)
                        company['prevvalue'].append("")
                except:
                    company['tag'].append('EV/LTM Revenue')
                    company['value'].append("")
                    company['prevpresent'].append(0)
                    company['prevvalue'].append("")

            if(k==0):
                try:
                    arrr =DerivedMetrics.objects.filter(Q(company__ticker = ticker2) & Q(tag = 'Annualized Revenue Run Rate (ARRR)') & Q(form_type='10-K')).order_by('-filing_date')
                    evarrr=ev/arrr[0].value
                    company['tag'].append('EV/Revenue Run rate')
                    company['value'].append(evarrr)
                    if (len(arrr)>=2):
                        company['prevpresent'].append(1)
                        evltm=evprev/arrr[1].value
                        company['prevvalue'].append(evltm)
                    else:
                        company['prevpresent'].append(0)
                        company['prevvalue'].append("")
                except:
                    company['tag'].append('EV/LTM Revenue')
                    company['value'].append("")
                    company['prevpresent'].append(0)
                    company['prevvalue'].append("")

            
            return JsonResponse(company, status=status.HTTP_201_CREATED, safe=False)
    except:       
    
        return JsonResponse({}, status=status.HTTP_400_BAD_REQUEST)

## API to fetch stock price history of a company from yahoo finance
@cache_page(60 * 60*2)
@api_view(['GET'])
def share_price(request):
    try:
        yf_dict={}
        start_date="12/04/1910"
        today = now.strftime("%Y/%m/%d")
        cik=str(request.GET['cik'])
        ticker=Companies.objects.filter(Q(cik = cik) )[0].ticker
        ticker2=ticker
        ticker=ticker.split(',')
        ticker=ticker[0].strip('[]')[1:-1]
        if request.method == 'GET':
            data= get_data(ticker, start_date=start_date, end_date=today, index_as_date = True)
            data = data[data.index >= datetime.strptime("2017-01-01", "%Y-%m-%d")   ]
            date_list=data.index.tolist()
            price_list=data['close'].tolist()
            yf_dict['date_list']=date_list
            yf_dict['price_list']=price_list
            date_10k=list(BaseMetrics.objects.filter(Q(company__cik = cik) & Q(form_type ='10-K')).values('filing_date').distinct())
            date_10q=list(BaseMetrics.objects.filter(Q(company__ticker = ticker2) &Q (form_type='10-Q')).values('filing_date').distinct())
            date_8K=list(BaseMetrics.objects.filter(Q(company__ticker = ticker2) &Q (form_type='8-K')).values('filing_date').distinct())
            
            date_10k = {x['filing_date']:1 for x in date_10k}
            date_10q = {x['filing_date']:1 for x in date_10q}
            date_8K = {x['filing_date']:1 for x in date_8K}
            yf_dict['category']=[]
            for x in yf_dict['date_list']:
                if(x.date() in date_10k):
                    yf_dict['category'].append("10-K")
                elif(x.date() in date_10q):
                    yf_dict['category'].append("10-Q")            
                elif(x.date() in date_8K):
                    yf_dict['category'].append("8-K")            
                else:
                    yf_dict['category'].append("")            
            
            return JsonResponse(yf_dict, status=status.HTTP_201_CREATED, safe=False)
    except:
        return JsonResponse({}, status=status.HTTP_400_BAD_REQUEST)

## API to generate word-frequency mapping from SEC filings for a particular comapny which is latr visualized as heat map  
@cache_page(60 * 60*2) 
@api_view(['GET'])
def heat_map(request):
    try:
        cik=str(request.GET['cik'])
        f = open(base+cik+'.json')
        data = json.load(f)
        return JsonResponse(data, status=status.HTTP_201_CREATED, safe=False)
    except:
        return JsonResponse({}, status=status.HTTP_400_BAD_REQUEST)

## API to get the list of derived metrics calculated for a company
@cache_page(60 * 60*2)
@api_view(['GET'])
def unique_metrics(request):
    try:
        if request.method == 'GET':
            derived_metrics = DerivedMetrics.objects.filter(company__cik=str(request.GET['cik']))
            if("tag" in request.GET):
                derived_metrics = derived_metrics.filter(tag=str(request.GET['tag']))
            if("form_type" in request.GET):
                derived_metrics = derived_metrics.filter(form_type=str(request.GET['form_type']))
            if("start_date" in request.GET):
                date = str(request.GET['start_date']).split('-')
                derived_metrics = derived_metrics.filter(filing_date__gte=datetime.date(int(date[2]), int(date[1]), int(date[0])))
            if("end_date" in request.GET):
                date = str(request.GET['start_date']).split('-')
                derived_metrics = derived_metrics.filter(filing_date__lte=datetime.date(int(date[2]), int(date[1]), int(date[0])))
            derived_metrics = derived_metrics.values_list('tag').distinct()
            list = []
            for x in derived_metrics:
                dict_ = {}
                tag = DerivedMetrics.objects.filter(tag=x[0])[0]
                dict_['sentence'] = tag.sentence
                dict_['score'] = tag.score
                dict_['description'] = tag.description
                dict_['source'] = tag.source
                dict_['formula'] = tag.formula
                dict_['tag'] = x[0]
                list.append(dict_)
            return JsonResponse(list, safe=False)
    except:
        return JsonResponse({}, status=status.HTTP_400_BAD_REQUEST)

## API to display the balance sheets, statements of income and cash flow of a particular company
@cache_page(60 * 60*2)
@api_view(['GET'])
def balance_sheet(request):
    headers= {'User-Agent': 'E-cellankit.bagde2000@ecell-iitkgp.org'}
    start_yr=2017
    end_yr=2022
    forms = ['10-K']
    cik_no = str(request.GET['cik'])
    cik_no = cik_no.zfill(10)
    submission_url = "https://data.sec.gov/submissions/CIK{}.json".format(cik_no)
    content = requests.get(submission_url, headers=headers)
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
        content = requests.get(normal_url, headers=headers)
        content=content.json()
        year=str(filingdate2[count]).split('-')[0]
        count+=1
        for file in content['directory']['item']:
    
            # Grab the filing summary and create a new url leading to the file so we can download it.
            if file['name'] == 'FilingSummary.xml':

                xml_summary = base_url + content['directory']['name'] + "/" + file['name']
                base_url = xml_summary.replace('FilingSummary.xml', '')

        content = requests.get(xml_summary, headers=headers).content
        soup = BeautifulSoup(content, 'lxml')
        reports = soup.find('myreports')
        time.sleep(2)
        master_reports = []
        reporttemp={}
        reporttemp['year']=year
        for report in reports.find_all('report')[:-1]:

            report_dict = {}
            report_dict['name_short'] = report.shortname.text
            report_dict['name_long'] = report.longname.text
            report_dict['position'] = report.position.text
            report_dict['category'] = report.menucategory.text
            report_dict['url'] = base_url + report.htmlfilename.text
            master_reports.append(report_dict)

        statements_url = []
        statementsname=[]
        for report_dict in master_reports:

            item1 = r"Consolidated Balance Sheets"
            item2 = r"Consolidated Statements Income"
            item3 = r"Consolidated Statements of Cash Flows"

            report_list = [item1, item2, item3]

            if item1 in report_dict['name_short'] or item2 in report_dict['name_short'] or item3 in report_dict['name_short'] :
                statements_url.append(report_dict['url'])
                statementsname.append(report_dict['name_short'] )

        k=0
        yr_data=[]
        for url in statements_url:
            headers2 = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            content = requests.get(url, headers=headers).content
            report_soup = BeautifulSoup(content, 'html')
            data=report_soup.findAll('table')[0]
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
            data_list['tablename']=statementsname[k]
            data_list['table_data']=(str(data))
            k+=1
            yr_data.append(data_list)
        reporttemp['data']=yr_data
        fin_data.append(reporttemp)
    return JsonResponse(fin_data, status=status.HTTP_201_CREATED, safe=False)

## API to fetch text metric for a particular company
@cache_page(60 * 60*2)
@api_view(['GET'])
def metric_plot(request):
    try:
        cik_no = str(request.GET['cik']) 
        met_list=list(RiskModel.objects.filter(Q(company__cik = cik_no)).order_by('filing_date'))
        yr=[]
        fin=[]
        idiosyncratic=[]
        legal=[]
        tax=[]
        systematic=[]
        for i in range (len(met_list)):
            yr.append(met_list[i].filing_date)
            fin.append(met_list[i].financial)
            idiosyncratic.append(met_list[i].otheridiosyncracies )
            legal.append(met_list[i].legal)
            tax.append(met_list[i].tax)
            systematic.append(met_list[i].othersystematic)
    
        plot={}
        plot['Year']=yr
        plot['Finnancial']=fin
        plot['IdiosyncraticS']=idiosyncratic
        plot['Legal']=legal
        plot['Tax']=tax
        plot['Systematic']=systematic
        return JsonResponse(plot, status=status.HTTP_201_CREATED, safe=False)
    except:
        return JsonResponse({}, status=status.HTTP_400_BAD_REQUEST)

##API to fetch sentiment analysis for filings of a particular company
@cache_page(60 * 60*2)
@api_view(['GET'])
def sentiment(request):
    try:
        cik=str(request.GET['cik'])
        base="dashboard_api/cik_data/10_K/"
        files = [filename for filename in os.listdir(base) if filename.startswith('10K_'+cik)]
        q10k=list(SentimentModel.objects.filter(Q(company__cik = cik)))
        final={}
        final['item']=[]
        final['filing_date']=[]
        final['confidence']=[]
        final['label']=[]
        final['positive']=[]
        final['negative']=[]
        final['text']=[]
        for i in range (len(q10k)):
            final['item'].append(q10k[i].item)
            final['filing_date'].append(q10k[i].filing_date)
            final['confidence'].append(q10k[i].confidence)
            final['label'].append(q10k[i].label)
            final['positive'].append(q10k[i].positive)
            final['negative'].append(q10k[i].negative)
            date=q10k[i].filing_date
            date=str(date).split('-')
            date2=date[0]+date[1]+date[2]
            filetemp=[filename for filename in files if filename.startswith("10K_"+cik+"_"+date2)]
            f = open(base+filetemp[0])
            data = json.load(f)
            final['text'].append(data[q10k[i].item])
        return JsonResponse(final, status=status.HTTP_201_CREATED, safe=False)
    except:
        return JsonResponse({}, status=status.HTTP_400_BAD_REQUEST)

## API to fetch text based metrics
@api_view(['GET'])
@cache_page(60 * 60*2)
def risk_metric(request):
    try:
        if request.method == 'GET':
            cik = RiskModel.objects.filter(company__cik=str(request.GET['cik']))
            risk={}
            risk['Year']=[]
            risk['Financial']=[]
            risk['Idiosyncratics']=[]
            risk['Legal']=[]
            risk['Systematic']=[]
            risk['Tax']=[]
           
            for i in (cik):
                risk['Year'].append(i.filing_date)
                risk['Financial'].append(i.financial)
                risk['Idiosyncratics'].append(i.otheridiosyncracies)
                risk['Legal'].append(i.legal)
                risk['Systematic'].append(i.othersystematic)
                risk['Tax'].append(i.tax)            
            return JsonResponse(risk, status=status.HTTP_201_CREATED, safe=False)
    except:
        return JsonResponse({}, status=status.HTTP_400_BAD_REQUEST)


@cache_page(60 * 60*2)
@api_view(['GET'])
def read_html(request):
    try:
        cik=str(request.GET['cik'])
        f = open(basehtml+'data'+cik+'.json')
        data = json.load(f)
        return JsonResponse(data, status=status.HTTP_201_CREATED, safe=False)
    except:
        return JsonResponse({}, status=status.HTTP_400_BAD_REQUEST)

## API to fetch the ownership details from yahoo finance
@cache_page(60 * 60*2)
@api_view(['GET'])
def ownership(request):
    try:
        cik=str(request.GET['cik'])
        ticker=Companies.objects.filter(Q(cik = cik) )[0].ticker
        ticker2=ticker
        ticker=ticker.split(',')
        ticker=ticker[0].strip('[]')[1:-1] 
        final={}
        temp={}
        x=si.get_holders(ticker)
        temp['Holder']=x['Direct Holders (Forms 3 and 4)']['Holder'].tolist()
        temp['Shares']=x['Direct Holders (Forms 3 and 4)']['Shares'].tolist()
        temp['Date Reported']=x['Direct Holders (Forms 3 and 4)']['Date Reported'].tolist()
        temp['% Out']=x['Direct Holders (Forms 3 and 4)']['% Out'].tolist()
        temp['Value']=x['Direct Holders (Forms 3 and 4)']['Value'].tolist()

        list_ = []
        for a,b,c,d,e in zip(temp['Holder'], temp['Shares'], temp['Date Reported'], temp['% Out'], temp['Value']):
            list_.append({'Holder':a, 'Shares':b, 'Date Reported':c, '% Out':d, 'Value':e})

        final['Direct Holders']=list_

        temp={}
        temp['Holder']=x['Top Institutional Holders']['Holder'].tolist()
        temp['Shares']=x['Top Institutional Holders']['Shares'].tolist()
        temp['Date Reported']=x['Top Institutional Holders']['Date Reported'].tolist()
        temp['% Out']=x['Top Institutional Holders']['% Out'].tolist()
        temp['Value']=x['Top Institutional Holders']['Value'].tolist()
        list_ = []
        for a,b,c,d,e in zip(temp['Holder'], temp['Shares'], temp['Date Reported'], temp['% Out'], temp['Value']):
            list_.append({'Holder':a, 'Shares':b, 'Date Reported':c, '% Out':d, 'Value':e})

        final['Top Institutional Holders']=list_
        return JsonResponse(final, status=status.HTTP_201_CREATED, safe=False)
    except:
         return JsonResponse({}, status=status.HTTP_400_BAD_REQUEST)

## API to do benchmarking of various metrics of selected comapnies
@cache_page(60 * 60*2)
@api_view(['GET'])
def benchmarking(request):
    try:
        if request.method == 'GET':
            ciks = request.GET['cik'].split(',')
            data = []
            ciks_name = {}
            for cik in ciks:
                if(os.path.exists("dashboard_api/cik_data/derived_metrics/"+cik+".json")):
                    data.extend(json.load(open("dashboard_api/cik_data/derived_metrics/"+cik+".json")))
                    ciks_name[cik] = data[-1]['company']['name']
            final={}
            unique_met=list(DerivedMetrics.objects.order_by().values_list('tag',flat=True).distinct())
            for met in unique_met:
                final[met]=[{},{},{},{},{},{}]
                for k in range(6):
                    final[met][k]['year']=str(2017+k)

            for i in range (len(ciks)):
                for key in final.keys():
                    for j in range(6):
                        final[key][j][ciks_name[ciks[i]]]=0
            #count=0
            #return JsonResponse(final, status=status.HTTP_201_CREATED, safe=False)
            for x in data:
                if(x['tag']=='Cash on Balance Sheet'):
                    continue
                if(x['tag']=='CAC Payback'):
                    x['tag'] = 'CAC'
                yr=int(str(x['filing_date']).split('-')[0])-2017
                if yr>=0:
                    if(x['company']['cik'] in ciks):
                            final[x['tag']][yr][x['company']['name']]=x['value']
            return JsonResponse(final, status=status.HTTP_201_CREATED, safe=False)
    except:
        return JsonResponse({}, status=status.HTTP_400_BAD_REQUEST)

## API to set email alerts
@api_view(['POST'])
def get_email(request):
    try:
        if request.method == 'POST':
            data = request.data['email']
            sns = boto3.client("sns")
            response = sns.subscribe(TopicArn=SNS_ARN, Protocol="email", Endpoint=data)
            print(response)
            return JsonResponse(data,status=status.HTTP_201_CREATED, safe=False )
    except:
        return JsonResponse({}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def get_otp(request):
    try:
        if request.method == 'POST':
            data = request.data['otp']
            return JsonResponse(data,status=status.HTTP_201_CREATED, safe=False )
    except:
        return JsonResponse({}, status=status.HTTP_400_BAD_REQUEST)




        

