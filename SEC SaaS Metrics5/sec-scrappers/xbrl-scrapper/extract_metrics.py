import pandas as pd
import numpy as np
import datetime
import os

BASE_PATH = os.path.expanduser('~/sec-scraper/data/parsed_data/xbrl/')
FILE_NAME = "master2017-22.csv"
OUTPUT_BASE_PATH = BASE_PATH + "metrics/derived_metrics/"

data = pd.read_csv(BASE_PATH+FILE_NAME)
data['FilingDate'] = pd.to_datetime(data['FilingDate'])
print(len(data))
data.head()

import json
def format_base_dep(x):
  j = {"tag":[], "date":[]}
  for i in x:
    j['tag'].append(i[0])
    j['date'].append(str(i[1]))
  return json.dumps(j)

def metric_calculation(df):

  output_df = pd.DataFrame(columns=['metric', 'value', 'formula','base_dependencies','filing_date','form_type','cik','accession_number'])


  # METRICS = ['total_debt', 'net cash', 'total_cash', 'Efficiency or Rule of 40','FCF','Changes in Working Capital'
  #       'ARRR_Employee','LTM_FCF_PERCENT','CURRENT_QUATER_FCF_PERCENT','OPERATING_INCOME_PERCENT'
  #       ,'EBITDA_PERCENT','EBITDA','OPEX_PER_EMPLOYEE','ARRR_CUSTOMER','ARR_CUSTOMER',
  #       'NET_NEW_ARR', 'ARRR','NTM_ARRR', 'LTM Revenue', 'current revenue', 'LAST_YEAR_RUN_RATE_REVENUE',
  #       'REVENUE_GROWTH_YOY','gross profit', 'gross margin','r&d margin','g&a margin',
  #       'magic number','payback period','CAC or cost of acquiring a customer','s&m margin',
  #       'enterprise value or EV','EV/ Revenue run rate','EV/LTM Revenue','Average Contract Value']

  master_dict = {}
  master_dict['LongTermDebt'] = {}
  master_dict['LiabilitiesCurrent'] = {}
  master_dict['ShortTermInvestments']={}
  master_dict['GrossProfit']={}
  master_dict['CashAndCashEquivalentsAtCarryingValue'] = {}
  master_dict['Liabilities'] = {}
  master_dict['EquitySecuritiesFvNi']={}
  master_dict['RevenueFromContractWithCustomerExcludingAssessedTax']={}
  master_dict['Revenues']={}
  master_dict['NetIncomeLoss']={}
  master_dict['DepreciationAndAmortization']={}
  master_dict['PaymentsToAcquirePropertyPlantAndEquipment']={}
  master_dict['PaymentsToAcquireLongtermInvestments']={}
  master_dict['OperatingIncomeLoss']={}
  master_dict['OperatingExpenses']={}
  master_dict['ResearchAndDevelopmentExpense']={}
  master_dict['ResearchAndDevelopmentExpensePolicy']={}
  master_dict['GeneralAndAdministrativeExpense']={}
  master_dict['SellingGeneralAndAdministrativeExpense']={}
  master_dict['MarketingExpense']={}
  master_dict['MarketingAndAdvertisingExpense']={}
  master_dict['DebtSecuritiesTradingAndAvailableForSale'] = {}
  master_dict['AssetsCurrent'] = {}
  master_dict['StockholdersEquity'] = {}
  master_dict['DepreciationDepletionAndAmortization'] = {}
  master_dict['PaymentsToAcquireBusinessesNetOfCashAcquired'] = {}

  master_dict1 = {}
  master_dict1['LongTermDebt'] = {}
  master_dict1['LiabilitiesCurrent'] = {}
  master_dict1['ShortTermInvestments']={}
  master_dict1['GrossProfit']={}
  master_dict1['CashAndCashEquivalentsAtCarryingValue'] = {}
  master_dict1['Liabilities'] = {}
  master_dict1['EquitySecuritiesFvNi']={}
  master_dict1['RevenueFromContractWithCustomerExcludingAssessedTax']={}
  master_dict1['Revenues']={}
  master_dict1['NetIncomeLoss']={}
  master_dict1['DepreciationAndAmortization']={}
  master_dict1['PaymentsToAcquirePropertyPlantAndEquipment']={}
  master_dict1['PaymentsToAcquireLongtermInvestments']={}
  master_dict1['OperatingIncomeLoss']={}
  master_dict1['OperatingExpenses']={}
  master_dict1['ResearchAndDevelopmentExpense']={}
  master_dict1['ResearchAndDevelopmentExpensePolicy']={}
  master_dict1['GeneralAndAdministrativeExpense']={}
  master_dict1['SellingGeneralAndAdministrativeExpense']={}
  master_dict1['MarketingExpense']={}
  master_dict1['MarketingAndAdvertisingExpense']={}
  master_dict1['DebtSecuritiesTradingAndAvailableForSale'] = {}
  master_dict1['AssetsCurrent'] = {}
  master_dict1['DepreciationDepletionAndAmortization'] = {}
  master_dict1['PaymentsToAcquireBusinessesNetOfCashAcquired'] = {}
  master_dict1['StockholdersEquity'] = {}


  for i in range(len(df)):
    tag = df.iloc[i]['xbrl_tag_name'].split(':')
    
    try:
      if(len(tag)==2 and tag[0]=='us-gaap' and tag[1] in master_dict ):
        val = float(str(df.iloc[i]['value']).replace(',', ''))
        if(not np.isnan(val)):
          if (int(val)!=0):
            if(df.iloc[i]['FilingDate'] not in master_dict[tag[1]]):
              master_dict[tag[1]][df.iloc[i]['FilingDate']] = []
              master_dict1[tag[1]][df.iloc[i]['FilingDate']] = {}
            master_dict[tag[1]][df.iloc[i]['FilingDate']].append(int(val))
            master_dict1[tag[1]][df.iloc[i]['FilingDate']]['form_type'] = df.iloc[i]['FormType']
            master_dict1[tag[1]][df.iloc[i]['FilingDate']]['cik'] = df.iloc[i]['CIK']
            master_dict1[tag[1]][df.iloc[i]['FilingDate']]['accession_number'] = df.iloc[i]['accession_no']
    except:
      continue 

  """
  Debt to Equity ==  us-gaap:Liabilities / us-gaap:StockholdersEquity
  """

  intersection = { x: max(master_dict['Liabilities'][x]) / max(master_dict['StockholdersEquity'][x])  for x in master_dict['StockholdersEquity'] if x in master_dict['Liabilities']}
  for x in intersection:
    temp_df = {'metric': 'Debt to Equity', 'value': intersection[x] , 'formula': 'Liabilities / StockholdersEquity','base_dependencies':format_base_dep([('us-gaap:StockholdersEquity',x),('us-gaap:Liabilities',x)]),'filing_date': x, 'form_type':master_dict1['Liabilities'][x]['form_type'] ,'cik':master_dict1['Liabilities'][x]['cik'],'accession_number':master_dict1['Liabilities'][x]['accession_number']}
    output_df = output_df.append(temp_df, ignore_index=True)


  """
  Total debt = (us-gaap:LongTermDebt + us-gaap:LiabilitiesCurrent) or (us-gaap:Liabilities)
  """
  intersection = { x:max(master_dict['LongTermDebt'][x]) + max(master_dict['LiabilitiesCurrent'][x]) for x in master_dict['LiabilitiesCurrent'] if x in master_dict['LongTermDebt']}
  union = set().union(*[intersection, master_dict['Liabilities']])
  
  for x in union:
    if(x in intersection):
      temp_df = {'metric': 'Total debt', 'value': intersection[x] , 'formula': 'LongTermDebt+LiabilitiesCurrent','base_dependencies':format_base_dep([('us-gaap:LongTermDebt',x),('us-gaap:LiabilitiesCurrent',x)]),'filing_date': x,'form_type':master_dict1['LongTermDebt'][x]['form_type'] ,'cik':master_dict1['LongTermDebt'][x]['cik'],'accession_number':master_dict1['LiabilitiesCurrent'][x]['accession_number'] }
      output_df = output_df.append(temp_df, ignore_index=True)
    else:
      temp_df = {'metric': 'Total debt', 'value': max(master_dict['Liabilities'][x]) , 'formula': 'Liabilities','base_dependencies':format_base_dep([('us-gaap:Liabilities',x)]),'filing_date': x,'form_type':master_dict1['Liabilities'][x]['form_type'] ,'cik':master_dict1['Liabilities'][x]['cik'],'accession_number':master_dict1['Liabilities'][x]['accession_number'] }
      output_df = output_df.append(temp_df, ignore_index=True)
  

  """
  Net Cash =us-gaap:CashAndCashEquivalentsAtCarryingValue - (us-gaap:Liabilities)
  """
  
  intersection = { x: max(master_dict['CashAndCashEquivalentsAtCarryingValue'][x]) - max(master_dict['Liabilities'][x]) for x in master_dict['Liabilities'] if x in master_dict['CashAndCashEquivalentsAtCarryingValue']}
  for x in intersection:
    temp_df = {'metric': 'Net Cash', 'value': intersection[x] , 'formula': 'CashAndCashEquivalentsAtCarryingValue - Liabilities','base_dependencies':format_base_dep([('us-gaap:CashAndCashEquivalentsAtCarryingValue',x),('us-gaap:Liabilities',x)]),'filing_date': x,'form_type':master_dict1['CashAndCashEquivalentsAtCarryingValue'][x]['form_type'] ,'cik':master_dict1['CashAndCashEquivalentsAtCarryingValue'][x]['cik'],'accession_number':master_dict1['CashAndCashEquivalentsAtCarryingValue'][x]['accession_number'] }
    output_df = output_df.append(temp_df, ignore_index=True)

  """
  Total Cash== us-gaap:ShortTermInvestments + us-gaap:CashAndCashEquivalentsAtCarryingValue or  us-gaap:CashAndCashEquivalentsAtCarryingValue 
  """
  
  for x in master_dict['CashAndCashEquivalentsAtCarryingValue']:
    if(x in master_dict['ShortTermInvestments']):
      temp_df = {'metric': 'Total Cash', 'value': max(master_dict['CashAndCashEquivalentsAtCarryingValue'][x]) + max(master_dict['ShortTermInvestments'][x]) , 'formula': 'ShortTermInvestments + CashAndCashEquivalentsAtCarryingValue','base_dependencies':format_base_dep([('us-gaap:CashAndCashEquivalentsAtCarryingValue',x),('us-gaap:ShortTermInvestments',x)]),'filing_date': x,'form_type':master_dict1['CashAndCashEquivalentsAtCarryingValue'][x]['form_type'] ,'cik':master_dict1['CashAndCashEquivalentsAtCarryingValue'][x]['cik'],'accession_number':master_dict1['CashAndCashEquivalentsAtCarryingValue'][x]['accession_number'] }
      output_df = output_df.append(temp_df, ignore_index=True)
    else:
      temp_df = {'metric': 'Total Cash', 'value': max(master_dict['CashAndCashEquivalentsAtCarryingValue'][x]), 'formula': 'CashAndCashEquivalentsAtCarryingValue','base_dependencies':format_base_dep([('us-gaap:CashAndCashEquivalentsAtCarryingValue',x)]),'filing_date': x,'form_type':master_dict1['CashAndCashEquivalentsAtCarryingValue'][x]['form_type'] ,'cik':master_dict1['CashAndCashEquivalentsAtCarryingValue'][x]['cik'],'accession_number':master_dict1['CashAndCashEquivalentsAtCarryingValue'][x]['accession_number'] }
      output_df = output_df.append(temp_df, ignore_index=True)
        
  """
  Working Capital==us-gaap:AssetsCurrent - us-gaap:LiabilitiesCurrent
  """

  intersection = { x: max(master_dict['AssetsCurrent'][x]) - max(master_dict['LiabilitiesCurrent'][x])  for x in master_dict['AssetsCurrent'] if x in master_dict['LiabilitiesCurrent']}
  for x in intersection:
    temp_df = {'metric': 'Working Capital', 'value': intersection[x] , 'formula': 'AssetsCurrent + LiabilitiesCurrent','base_dependencies':format_base_dep([('us-gaap:AssetsCurrent',x),('us-gaap:LiabilitiesCurrent',x)]),'filing_date': x, 'form_type':master_dict1['AssetsCurrent'][x]['form_type'] ,'cik':master_dict1['AssetsCurrent'][x]['cik'],'accession_number':master_dict1['AssetsCurrent'][x]['accession_number']}
    output_df = output_df.append(temp_df, ignore_index=True)

  """
  Depreciation = us-gaap:DepreciationDepletionAndAmortization   or us-gaap:DepreciationAndAmortization
  """
  union = set().union(*[master_dict['DepreciationAndAmortization'], master_dict['DepreciationDepletionAndAmortization']])
  for x in union:
    if(x in master_dict['DepreciationAndAmortization']):
      # print(master_dict['DepreciationAndAmortization'][x])
      temp_df = {'metric': 'Depreciation', 'value': max(master_dict['DepreciationAndAmortization'][x]) , 'formula': 'DepreciationAndAmortization','base_dependencies':format_base_dep([('us-gaap:DepreciationAndAmortization',x)]),'filing_date': x,'form_type':master_dict1['DepreciationAndAmortization'][x]['form_type'] ,'cik':master_dict1['DepreciationAndAmortization'][x]['cik'],'accession_number':master_dict1['DepreciationAndAmortization'][x]['accession_number']}
      output_df = output_df.append(temp_df, ignore_index=True)
    else:
      temp_df = {'metric': 'Depreciation', 'value': max(master_dict['DepreciationDepletionAndAmortization'][x]) , 'formula': 'DepreciationDepletionAndAmortization','base_dependencies':format_base_dep([('us-gaap:DepreciationDepletionAndAmortization',x)]),'filing_date': x,'form_type':master_dict1['DepreciationDepletionAndAmortization'][x]['form_type'] ,'cik':master_dict1['DepreciationDepletionAndAmortization'][x]['cik'],'accession_number':master_dict1['DepreciationDepletionAndAmortization'][x]['accession_number']}
      output_df = output_df.append(temp_df, ignore_index=True)
  
  """
  Changes in working capital = (us-gaap:PaymentsToAcquireBusinessesNetOfCashAcquired + us-gaap:PaymentsToAcquirePropertyPlantAndEquipment ) or 
    (us-gaap:PaymentsToAcquirePropertyPlantAndEquipment + us-gaap:PaymentsToAcquireLongtermInvestments)
  """
  intersection1 = { x: max(master_dict['PaymentsToAcquireBusinessesNetOfCashAcquired'][x]) + max(master_dict['PaymentsToAcquirePropertyPlantAndEquipment'][x]) for x in master_dict['PaymentsToAcquireBusinessesNetOfCashAcquired'] if x in master_dict['PaymentsToAcquirePropertyPlantAndEquipment']}
  intersection2 = { x: max(master_dict['PaymentsToAcquirePropertyPlantAndEquipment'][x]) - max(master_dict['PaymentsToAcquireLongtermInvestments'][x]) for x in master_dict['PaymentsToAcquirePropertyPlantAndEquipment'] if x in master_dict['PaymentsToAcquireLongtermInvestments']}
  union = set().union(*[intersection1, intersection2])
  for x in union:
    if(x in intersection1):
      temp_df = {'metric': 'Changes in working capital', 'value': intersection1[x] , 'formula': 'PaymentsToAcquireBusinessesNetOfCashAcquired + PaymentsToAcquirePropertyPlantAndEquipment ','base_dependencies':format_base_dep([('us-gaap:PaymentsToAcquireBusinessesNetOfCashAcquired',x),('us-gaap:PaymentsToAcquirePropertyPlantAndEquipment',x)]),'filing_date': x,'form_type':master_dict1['PaymentsToAcquireBusinessesNetOfCashAcquired'][x]['form_type'] ,'cik':master_dict1['PaymentsToAcquireBusinessesNetOfCashAcquired'][x]['cik'],'accession_number':master_dict1['PaymentsToAcquireBusinessesNetOfCashAcquired'][x]['accession_number']}
      output_df = output_df.append(temp_df, ignore_index=True)
    else:
      temp_df = {'metric': 'Changes in working capital', 'value': intersection2[x] , 'formula': 'PaymentsToAcquirePropertyPlantAndEquipment + PaymentsToAcquireLongtermInvestments','base_dependencies':format_base_dep([('us-gaap:PaymentsToAcquirePropertyPlantAndEquipment',x),('us-gaap:PaymentsToAcquireLongtermInvestments',x)]),'filing_date': x,'form_type':master_dict1['PaymentsToAcquirePropertyPlantAndEquipment'][x]['form_type'] ,'cik':master_dict1['PaymentsToAcquirePropertyPlantAndEquipment'][x]['cik'],'accession_number':master_dict1['PaymentsToAcquirePropertyPlantAndEquipment'][x]['accession_number']}
      output_df = output_df.append(temp_df, ignore_index=True)
  
  """
  Operating Income % = us-gaap:OperatingIncomeLoss/(us-gaap:Revenues or us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax)
  """
  intersection1 = { x: max(master_dict['OperatingIncomeLoss'][x]) / max(master_dict['Revenues'][x]) for x in master_dict['OperatingIncomeLoss'] if x in master_dict['Revenues']}
  intersection2 = { x: max(master_dict['OperatingIncomeLoss'][x]) / max(master_dict['RevenueFromContractWithCustomerExcludingAssessedTax'][x]) for x in master_dict['OperatingIncomeLoss'] if x in master_dict['RevenueFromContractWithCustomerExcludingAssessedTax']}
  union = set().union(*[intersection1, intersection2])
  for x in union:
    if(x in intersection1 and master_dict1['OperatingIncomeLoss'][x]['form_type']=="10-K" and master_dict1['Revenues'][x]['form_type']=="10-K"):
      temp_df = {'metric': 'Operating Income %', 'value': intersection1[x] , 'formula': 'OperatingIncomeLoss / Revenues','base_dependencies':format_base_dep([('us-gaap:OperatingIncomeLoss',x),('us-gaap:Revenues',x)]),'filing_date': x,'form_type':master_dict1['Revenues'][x]['form_type'] ,'cik':master_dict1['Revenues'][x]['cik'],'accession_number':master_dict1['Revenues'][x]['accession_number']}
      output_df = output_df.append(temp_df, ignore_index=True)
    elif(x in intersection2 and master_dict1['OperatingIncomeLoss'][x]=="10-K" and master_dict1['RevenueFromContractWithCustomerExcludingAssessedTax'][x]=="10-K"):
      temp_df = {'metric': 'Operating Income %', 'value': intersection2[x] , 'formula': 'OperatingIncomeLoss / RevenueFromContractWithCustomerExcludingAssessedTax','base_dependencies':format_base_dep([('us-gaap:OperatingIncomeLoss',x),('us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax',x)]),'filing_date': x,'form_type':master_dict1['RevenueFromContractWithCustomerExcludingAssessedTax'][x]['form_type'] ,'cik':master_dict1['RevenueFromContractWithCustomerExcludingAssessedTax'][x]['cik'],'accession_number':master_dict1['RevenueFromContractWithCustomerExcludingAssessedTax'][x]['accession_number']}
      output_df = output_df.append(temp_df, ignore_index=True)
  
  
  """
  EBITDA% = us-gaap:NetIncomeLoss/(us-gaap:Revenues or us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax)
  """
  intersection1 = { x: max(master_dict['NetIncomeLoss'][x]) / max(master_dict['Revenues'][x]) for x in master_dict['Revenues'] if x in master_dict['NetIncomeLoss']}
  intersection2 = { x: max(master_dict['NetIncomeLoss'][x]) / max(master_dict['RevenueFromContractWithCustomerExcludingAssessedTax'][x]) for x in master_dict['RevenueFromContractWithCustomerExcludingAssessedTax'] if x in master_dict['NetIncomeLoss']}
  union = set().union(*[intersection1, intersection2])
  for x in union:
    if(x in intersection1 and master_dict1['NetIncomeLoss'][x]=="10-K" and master_dict1['Revenues'][x]=="10-K"):
      temp_df = {'metric': 'EBITDA %', 'value': intersection1[x] , 'formula': 'NetIncomeLoss/Revenues','base_dependencies':format_base_dep([('us-gaap:NetIncomeLoss',x),('us-gaap:Revenues',x)]),'filing_date': x,'form_type':master_dict1['Revenues'][x]['form_type'] ,'cik':master_dict1['Revenues'][x]['cik'],'accession_number':master_dict1['Revenues'][x]['accession_number']}
      output_df = output_df.append(temp_df, ignore_index=True)
    elif(x in intersection2 and master_dict1['NetIncomeLoss'][x]=="10-K" and master_dict1['RevenueFromContractWithCustomerExcludingAssessedTax'][x]=="10-K"):
      temp_df = {'metric': 'EBITDA %', 'value': intersection2[x] , 'formula': 'NetIncomeLoss/RevenueFromContractWithCustomerExcludingAssessedTax','base_dependencies':format_base_dep([('us-gaap:NetIncomeLoss',x),('us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax',x)]),'filing_date': x,'form_type':master_dict1['RevenueFromContractWithCustomerExcludingAssessedTax'][x]['form_type'] ,'cik':master_dict1['RevenueFromContractWithCustomerExcludingAssessedTax'][x]['cik'],'accession_number':master_dict1['RevenueFromContractWithCustomerExcludingAssessedTax'][x]['accession_number']}
      output_df = output_df.append(temp_df, ignore_index=True)
  

  """
  EBITDA = NetIncomeLoss
  """
  for x in master_dict['NetIncomeLoss']:
    temp_df = {'metric': 'NetIncomeLoss', 'value': max(master_dict['NetIncomeLoss'][x]) , 'formula': 'NetIncomeLoss','base_dependencies':format_base_dep([('us-gaap:NetIncomeLoss',x)]),'filing_date': x,'form_type':master_dict1['NetIncomeLoss'][x]['form_type'] ,'cik':master_dict1['NetIncomeLoss'][x]['cik'],'accession_number':master_dict1['NetIncomeLoss'][x]['accession_number']}
    output_df = output_df.append(temp_df, ignore_index=True)

  """
  Annualized Revenue Run Rate (ARRR) = (us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax)*4   or (us-gaap:Revenues)*4
  """ 
  union = set().union(*[master_dict['RevenueFromContractWithCustomerExcludingAssessedTax'], master_dict['Revenues']])
  for x in union:
    if(x in master_dict['RevenueFromContractWithCustomerExcludingAssessedTax']):
      temp_df = {'metric': 'Annualized Revenue Run Rate (ARRR)', 'value': max(master_dict['RevenueFromContractWithCustomerExcludingAssessedTax'][x])*4 , 'formula': 'RevenueFromContractWithCustomerExcludingAssessedTax*4','base_dependencies':format_base_dep([('us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax',x)]),'filing_date': x,'form_type':master_dict1['RevenueFromContractWithCustomerExcludingAssessedTax'][x]['form_type'] ,'cik':master_dict1['RevenueFromContractWithCustomerExcludingAssessedTax'][x]['cik'],'accession_number':master_dict1['RevenueFromContractWithCustomerExcludingAssessedTax'][x]['accession_number']}
      output_df = output_df.append(temp_df, ignore_index=True)
    else:
      temp_df = {'metric': 'Annualized Revenue Run Rate (ARRR)', 'value': max(master_dict['Revenues'][x])*4 , 'formula': 'Revenues*4','base_dependencies':format_base_dep([('us-gaap:Revenues',x)]),'filing_date': x,'form_type':master_dict1['Revenues'][x]['form_type'] ,'cik':master_dict1['Revenues'][x]['cik'],'accession_number':master_dict1['Revenues'][x]['accession_number']}
      output_df = output_df.append(temp_df, ignore_index=True)
  
  """
  Gross Margin = us-gaap:GrossProfit/(us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax) or (us-gaap:Revenues)  
  """
  intersection1 = { x: max(master_dict['GrossProfit'][x]) / max(master_dict['Revenues'][x]) for x in master_dict['GrossProfit'] if x in master_dict['Revenues']}
  intersection2 = { x: max(master_dict['GrossProfit'][x]) / max(master_dict['RevenueFromContractWithCustomerExcludingAssessedTax'][x]) for x in master_dict['GrossProfit'] if x in master_dict['RevenueFromContractWithCustomerExcludingAssessedTax']}
  union = set().union(*[intersection1, intersection2])
  for x in union:
    if(x in intersection1):
      temp_df = {'metric': 'Gross Margin', 'value': intersection1[x] , 'formula': 'GrossProfit / Revenues','base_dependencies':format_base_dep([('us-gaap:GrossProfit',x),('us-gaap:Revenues',x)]),'filing_date': x,'form_type':master_dict1['Revenues'][x]['form_type'] ,'cik':master_dict1['Revenues'][x]['cik'],'accession_number':master_dict1['Revenues'][x]['accession_number']}
      output_df = output_df.append(temp_df, ignore_index=True)
    else:
      temp_df = {'metric': 'Gross Margin', 'value': intersection2[x] , 'formula': 'GrossProfit / RevenueFromContractWithCustomerExcludingAssessedTax','base_dependencies':format_base_dep([('us-gaap:GrossProfit',x),('us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax',x)]),'filing_date': x,'form_type':master_dict1['RevenueFromContractWithCustomerExcludingAssessedTax'][x]['form_type'] ,'cik':master_dict1['RevenueFromContractWithCustomerExcludingAssessedTax'][x]['cik'],'accession_number':master_dict1['RevenueFromContractWithCustomerExcludingAssessedTax'][x]['accession_number']}
      output_df = output_df.append(temp_df, ignore_index=True)
    
  """
  Current Revenue = us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax or us-gaap:Revenues 
  """
  union = set().union(*[master_dict['RevenueFromContractWithCustomerExcludingAssessedTax'], master_dict['Revenues']])
  for x in union:
    if(x in master_dict['RevenueFromContractWithCustomerExcludingAssessedTax'] and master_dict1['RevenueFromContractWithCustomerExcludingAssessedTax'][x]=='10-Q'):
      temp_df = {'metric': 'Current Revenue', 'value': max(master_dict['RevenueFromContractWithCustomerExcludingAssessedTax'][x]) , 'formula': 'RevenueFromContractWithCustomerExcludingAssessedTax','base_dependencies':format_base_dep([('us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax',x)]),'filing_date': x,'form_type':master_dict1['RevenueFromContractWithCustomerExcludingAssessedTax'][x]['form_type'] ,'cik':master_dict1['RevenueFromContractWithCustomerExcludingAssessedTax'][x]['cik'],'accession_number':master_dict1['RevenueFromContractWithCustomerExcludingAssessedTax'][x]['accession_number']}
      output_df = output_df.append(temp_df, ignore_index=True)
    elif(x in master_dict['Revenues'] and master_dict1['Revenues'][x]=='10-Q'):
      temp_df = {'metric': 'Current Revenue', 'value': max(master_dict['Revenues'][x]) , 'formula': 'Revenues','base_dependencies':format_base_dep([('us-gaap:Revenues',x)]),'filing_date': x,'form_type':master_dict1['Revenues'][x]['form_type'] ,'cik':master_dict1['Revenues'][x]['cik'],'accession_number':master_dict1['Revenues'][x]['accession_number']}
      output_df = output_df.append(temp_df, ignore_index=True)
  
  """
  S&M Margin = (us-gaap:MarketingExpense or us-gaap:MarketingAndAdvertisingExpense) / (us-gaap:Revenues or us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax)
  """
  union1 = set().union(*[master_dict['MarketingExpense'], master_dict['MarketingAndAdvertisingExpense']])
  union2 = set().union(*[master_dict['Revenues'], master_dict['RevenueFromContractWithCustomerExcludingAssessedTax']])
  intersection = {}
  for x in union1:
    if(x in union2):
      temp_df=None
      if(x in master_dict['MarketingExpense'] and x in master_dict['Revenues'] and master_dict1['MarketingExpense'][x]=="10-Q" and master_dict1['Revenues'][x]=="10-Q"):
        intersection[x] = max(master_dict['MarketingExpense'][x]) / max(master_dict['Revenues'][x])
        temp_df = {'metric': 'S&M Margin', 'value': intersection[x] , 'formula': 'MarketingExpense / Revenues','base_dependencies':format_base_dep([('us-gaap:Revenues',x),('us-gaap:MarketingExpense',x)]),'filing_date': x,'form_type':master_dict1['MarketingAndAdvertisingExpense'][x]['form_type'] ,'cik':cik,'accession_number':master_dict1['MarketingExpense'][x]['MarketingAndAdvertisingExpense']}

      elif(x in master_dict['MarketingAndAdvertisingExpense'] and x in master_dict['Revenues'] and master_dict1['MarketingAndAdvertisingExpense'][x]=="10-Q" and master_dict1['Revenues'][x]=="10-Q"):      
        intersection[x] = max(master_dict['MarketingAndAdvertisingExpense'][x]) / max(master_dict['Revenues'][x])
        temp_df = {'metric': 'S&M Margin', 'value': intersection[x] , 'formula': 'MarketingAndAdvertisingExpense / Revenues','base_dependencies':format_base_dep([('us-gaap:Revenues',x),('us-gaap:MarketingAndAdvertisingExpense',x)]),'filing_date': x,'form_type':master_dict1['MarketingAndAdvertisingExpense'][x]['form_type'] ,'cik':cik,'accession_number':master_dict1['MarketingExpense'][x]['MarketingAndAdvertisingExpense']}

      elif(x in master_dict['MarketingExpense'] and x in master_dict['RevenueFromContractWithCustomerExcludingAssessedTax'] and master_dict1['MarketingExpense'][x]=="10-Q" and master_dict1['RevenueFromContractWithCustomerExcludingAssessedTax'][x]=="10-Q"):      
        intersection[x] = max(master_dict['MarketingExpense'][x]) / max(master_dict['RevenueFromContractWithCustomerExcludingAssessedTax'][x])
        temp_df = {'metric': 'S&M Margin', 'value': intersection[x] , 'formula': 'MarketingExpense / RevenueFromContractWithCustomerExcludingAssessedTax','base_dependencies':format_base_dep([('us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax',x),('us-gaap:MarketingExpense',x)]),'filing_date': x,'form_type':master_dict1['MarketingAndAdvertisingExpense'][x]['form_type'] ,'cik':cik,'accession_number':master_dict1['MarketingExpense'][x]['MarketingAndAdvertisingExpense']}

      elif(x in master_dict['MarketingAndAdvertisingExpense'] and x in master_dict['RevenueFromContractWithCustomerExcludingAssessedTax'] and master_dict1['MarketingAndAdvertisingExpense'][x]=="10-Q" and master_dict1['RevenueFromContractWithCustomerExcludingAssessedTax'][x]=="10-Q"):      
        intersection[x] = max(master_dict['MarketingAndAdvertisingExpense'][x]) / max(master_dict['RevenueFromContractWithCustomerExcludingAssessedTax'][x])
        temp_df = {'metric': 'S&M Margin', 'value': intersection[x] , 'formula': 'MarketingAndAdvertisingExpense / RevenueFromContractWithCustomerExcludingAssessedTax','base_dependencies':format_base_dep([('us-gaap:Revenues',x),('us-gaap:MarketingAndAdvertisingExpense',x)]),'filing_date': x,'form_type':master_dict1['MarketingAndAdvertisingExpense'][x]['form_type'] ,'cik':cik,'accession_number':master_dict1['MarketingExpense'][x]['MarketingAndAdvertisingExpense']}
      if(temp_df != None):
          output_df = output_df.append(temp_df, ignore_index=True)
    
  """
  G&A Margin = =(us-gaap:GeneralAndAdministrativeExpense  or  us-gaap:SellingGeneralAndAdministrativeExpense) /((us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax)   or (us-gaap:Revenues) )
  """
  union1 = set().union(*[master_dict['GeneralAndAdministrativeExpense'], master_dict['SellingGeneralAndAdministrativeExpense']])
  union2 = set().union(*[master_dict['Revenues'], master_dict['RevenueFromContractWithCustomerExcludingAssessedTax']])
  intersection = {}
  for x in union1:

    if(x in union2):
      temp_df=None
      if(x in master_dict['GeneralAndAdministrativeExpense'] and x in master_dict['Revenues'] and  master_dict1['Revenues'][x]=='10-Q' and master_dict1['GeneralAndAdministrativeExpense'][x]=='10-Q'):
        intersection[x] = max(master_dict['GeneralAndAdministrativeExpense'][x]) / max(master_dict['Revenues'][x])
        temp_df = {'metric': 'G&A Margin', 'value': intersection[x] , 'formula': 'GeneralAndAdministrativeExpense / Revenues','base_dependencies':format_base_dep([('us-gaap:GeneralAndAdministrativeExpense',x),('us-gaap:Revenues',x)]),'filing_date': x,'form_type':master_dict1['MarketingAndAdvertisingExpense'][x]['form_type'] ,'cik':cik,'accession_number':master_dict1['MarketingExpense'][x]['MarketingAndAdvertisingExpense']}

      elif(x in master_dict['SellingGeneralAndAdministrativeExpense'] and x in master_dict['Revenues'] and master_dict1['Revenues'][x]=='10-Q' and master_dict1['SellingGeneralAndAdministrativeExpense'][x]=='10-Q'):      
        intersection[x] = max(master_dict['SellingGeneralAndAdministrativeExpense'][x]) / max(master_dict['Revenues'][x])
        temp_df = {'metric': 'G&A Margin', 'value': intersection[x] , 'formula': 'SellingGeneralAndAdministrativeExpense / Revenues','base_dependencies':format_base_dep([('us-gaap:Revenues',x),('us-gaap:SellingGeneralAndAdministrativeExpense',x)]),'filing_date': x,'form_type':master_dict1['MarketingAndAdvertisingExpense'][x]['form_type'] ,'cik':cik,'accession_number':master_dict1['MarketingExpense'][x]['MarketingAndAdvertisingExpense']}

      elif(x in master_dict['GeneralAndAdministrativeExpense'] and x in master_dict['RevenueFromContractWithCustomerExcludingAssessedTax'] and master_dict1['RevenueFromContractWithCustomerExcludingAssessedTax'][x]=='10-Q' and master_dict1['GeneralAndAdministrativeExpense'][x]=='10-Q'):      
        intersection[x] = max(master_dict['GeneralAndAdministrativeExpense'][x]) / max(master_dict['RevenueFromContractWithCustomerExcludingAssessedTax'][x])
        temp_df = {'metric': 'G&A Margin', 'value': intersection[x] , 'formula': 'GeneralAndAdministrativeExpense / RevenueFromContractWithCustomerExcludingAssessedTax','base_dependencies':format_base_dep([('us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax',x),('us-gaap:GeneralAndAdministrativeExpense',x)]),'filing_date': x,'form_type':master_dict1['MarketingAndAdvertisingExpense'][x]['form_type'] ,'cik':cik,'accession_number':master_dict1['MarketingExpense'][x]['MarketingAndAdvertisingExpense']}

      elif(x in master_dict['SellingGeneralAndAdministrativeExpense'] and x in master_dict['RevenueFromContractWithCustomerExcludingAssessedTax'] and master_dict1['RevenueFromContractWithCustomerExcludingAssessedTax'][x]=='10-Q' and master_dict1['SellingGeneralAndAdministrativeExpense'][x]=='10-Q'):      
        intersection[x] = max(master_dict['SellingGeneralAndAdministrativeExpense'][x]) / max(master_dict['RevenueFromContractWithCustomerExcludingAssessedTax'][x])
        temp_df = {'metric': 'G&A Margin', 'value': intersection[x] , 'formula': 'SellingGeneralAndAdministrativeExpense / RevenueFromContractWithCustomerExcludingAssessedTax','base_dependencies':format_base_dep([('us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax',x),('us-gaap:SellingGeneralAndAdministrativeExpense',x)]),'filing_date': x,'form_type':master_dict1['MarketingAndAdvertisingExpense'][x]['form_type'] ,'cik':cik,'accession_number':master_dict1['MarketingExpense'][x]['MarketingAndAdvertisingExpense']}
      if(temp_df != None):
        output_df = output_df.append(temp_df, ignore_index=True)

  """
  R&D Margin = us-gaap:ResearchAndDevelopmentExpense or us-gaap:ResearchAndDevelopmentExpensePolicy or  / ((us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax)   or (us-gaap:Revenues) )
  """
  union1 = set().union(*[master_dict['ResearchAndDevelopmentExpense'], master_dict['ResearchAndDevelopmentExpensePolicy']])
  union2 = set().union(*[master_dict['Revenues'], master_dict['RevenueFromContractWithCustomerExcludingAssessedTax']])
  intersection = {}
  for x in union1:
    if(x in union2):
      temp_df=None
      if(x in master_dict['ResearchAndDevelopmentExpense'] and x in master_dict['Revenues'] and master_dict1['Revenues'][x]=='10-Q' and master_dict1['ResearchAndDevelopmentExpense'][x]=='10-Q'):
        intersection[x] = max(master_dict['ResearchAndDevelopmentExpense'][x]) / max(master_dict['Revenues'][x])
        temp_df = {'metric': 'R&D Margin', 'value': intersection[x] , 'formula': 'ResearchAndDevelopmentExpense / Revenues','base_dependencies':format_base_dep([('us-gaap:ResearchAndDevelopmentExpense',x),('us-gaap:Revenues',x)]),'filing_date': x,'form_type':master_dict1['MarketingAndAdvertisingExpense'][x]['form_type'] ,'cik':cik,'accession_number':master_dict1['MarketingExpense'][x]['MarketingAndAdvertisingExpense']}

      elif(x in master_dict['ResearchAndDevelopmentExpensePolicy'] and x in master_dict['Revenues'] and master_dict1['Revenues'][x]=='10-Q' and master_dict1['ResearchAndDevelopmentExpensePolicy'][x]=='10-Q'):      
        intersection[x] = max(master_dict['ResearchAndDevelopmentExpensePolicy'][x]) / max(master_dict['Revenues'][x])
        temp_df = {'metric': 'R&D Margin', 'value': intersection[x] , 'formula': 'ResearchAndDevelopmentExpensePolicy / Revenues','base_dependencies':format_base_dep([('us-gaap:ResearchAndDevelopmentExpensePolicy',x),('us-gaap:Revenues',x)]),'filing_date': x,'form_type':master_dict1['MarketingAndAdvertisingExpense'][x]['form_type'] ,'cik':cik,'accession_number':master_dict1['MarketingExpense'][x]['MarketingAndAdvertisingExpense']}

      elif(x in master_dict['ResearchAndDevelopmentExpense'] and x in master_dict['RevenueFromContractWithCustomerExcludingAssessedTax'] and master_dict1['ResearchAndDevelopmentExpense'][x]=='10-Q' and master_dict1['RevenueFromContractWithCustomerExcludingAssessedTax'][x]=='10-Q'):      
        intersection[x] = max(master_dict['ResearchAndDevelopmentExpense'][x]) / max(master_dict['RevenueFromContractWithCustomerExcludingAssessedTax'][x])
        temp_df = {'metric': 'R&D Margin', 'value': intersection[x] , 'formula':'ResearchAndDevelopmentExpense / RevenueFromContractWithCustomerExcludingAssessedTax','base_dependencies':format_base_dep([('us-gaap:ResearchAndDevelopmentExpense',x),('us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax',x)]),'filing_date': x,'form_type':master_dict1['MarketingAndAdvertisingExpense'][x]['form_type'] ,'cik':cik,'accession_number':master_dict1['MarketingExpense'][x]['MarketingAndAdvertisingExpense']}

      elif(x in master_dict['ResearchAndDevelopmentExpensePolicy'] and x in master_dict['RevenueFromContractWithCustomerExcludingAssessedTax'] and master_dict1['RevenueFromContractWithCustomerExcludingAssessedTax'][x]=='10-Q' and master_dict1['ResearchAndDevelopmentExpensePolicy'][x]=='10-Q'):      
        intersection[x] = max(master_dict['ResearchAndDevelopmentExpensePolicy'][x]) / max(master_dict['RevenueFromContractWithCustomerExcludingAssessedTax'][x])
        temp_df = {'metric': 'R&D Margin', 'value': intersection[x] , 'formula': 'ResearchAndDevelopmentExpensePolicy / RevenueFromContractWithCustomerExcludingAssessedTax','base_dependencies':format_base_dep([('us-gaap:ResearchAndDevelopmentExpensePolicy',x),('us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax',x)]),'filing_date': x,'form_type':master_dict1['MarketingAndAdvertisingExpense'][x]['form_type'] ,'cik':cik,'accession_number':master_dict1['MarketingExpense'][x]['MarketingAndAdvertisingExpense']}  
      if(temp_df != None):
        output_df = output_df.append(temp_df, ignore_index=True)

  
  """
  NTM ARR = Current Revenue * (1 + Current Revenue Growth Rate * 85%)
  CUrrent Growth Rate =  (latest revenue 10K - previous revenue 10K)/ (previous revenue 10K)
  us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax or us-gaap:Revenues
  """
  rfcwea = [ (x, max(master_dict['RevenueFromContractWithCustomerExcludingAssessedTax'][x])) for x in sorted(master_dict['RevenueFromContractWithCustomerExcludingAssessedTax'])]
  revenues = [ (x, max(master_dict['Revenues'][x])) for x in sorted(master_dict['Revenues'])]
  done_x = {}
  for i in range(len(rfcwea)-1, 0, -1):
    # check if both are from 10-K
    if(master_dict1['RevenueFromContractWithCustomerExcludingAssessedTax'][rfcwea[i][0]]=="10-K" and master_dict1['RevenueFromContractWithCustomerExcludingAssessedTax'][rfcwea[i-1][0]]=="10-K"):
      if(rfcwea[i][0]-rfcwea[i-1][0] < datetime.timedelta(days=400)):
        done_x[rfcwea[i][0]]=1
        temp_df = {'metric': 'NTM ARR', 'value': rfcwea[i][1]*(1+((rfcwea[i][1] - rfcwea[i-1][1])*0.85)/rfcwea[i-1][1]) , 'formula': 'Current Revenue * (1 + Current Revenue Growth Rate * 85%)','base_dependencies':format_base_dep([('us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax',rfcwea[i][0]), ('us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax',rfcwea[i-1][0])]),'filing_date': rfcwea[i][0],'form_type':master_dict1['RevenueFromContractWithCustomerExcludingAssessedTax'][x]['form_type'] ,'cik':cik,'accession_number':master_dict1['RevenueFromContractWithCustomerExcludingAssessedTax'][x]['accession_number']}
        output_df = output_df.append(temp_df, ignore_index=True)
  
  for i in range(len(revenues)-1, 0, -1):
    # check if both are from 10-K
    if(master_dict1['Revenues'][revenues[i][0]]=="10-K" and master_dict1['Revenues'][revenues[i-1][0]]=="10-K" and revenues[i][0] not in done_x):
      if(rfcwea[i][0]-revenues[i-1][0] < datetime.timedelta(days=600)):
        done_x[revenues[i][0]]=1
        temp_df = {'metric': 'NTM ARR', 'value': revenues[i][1]*(1+((revenues[i][1] - revenues[i-1][1])*0.85)/revenues[i-1][1]) , 'formula': 'Current Revenue * (1 + Current Revenue Growth Rate * 85%)','base_dependencies':format_base_dep([('us-gaap:Revenues',revenues[i][0]), ('us-gaap:Revenues',revenues[i-1][0])]),'filing_date': revenues[i][0],'form_type':master_dict1['Revenues'][x]['form_type'] ,'cik':cik,'accession_number':master_dict1['Revenues'][x]['accession_number']}
        output_df = output_df.append(temp_df, ignore_index=True)

  """
  LTM Revenue= =us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax  or us-gaap:Revenues
  """
  union = set().union(*[master_dict['RevenueFromContractWithCustomerExcludingAssessedTax'], master_dict['Revenues']])
  for x in union:
    if (x in master_dict['RevenueFromContractWithCustomerExcludingAssessedTax'] and master_dict1['RevenueFromContractWithCustomerExcludingAssessedTax'][x]['form_type']=='10-K'):
      temp_df = {'metric': 'LTM Revenue', 'value': max(master_dict['RevenueFromContractWithCustomerExcludingAssessedTax'][x]) , 'formula': 'RevenueFromContractWithCustomerExcludingAssessedTax', 'base_dependencies':format_base_dep([('us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax',x)]), 'filing_date': x,'form_type':master_dict1['RevenueFromContractWithCustomerExcludingAssessedTax'][x]['form_type'] ,'cik':master_dict1['RevenueFromContractWithCustomerExcludingAssessedTax'][x]['cik'],'accession_number':master_dict1['RevenueFromContractWithCustomerExcludingAssessedTax'][x]['accession_number']}
      output_df = output_df.append(temp_df, ignore_index=True)
    elif(x in master_dict['Revenues'] and master_dict1['Revenues'][x]['form_type']=='10-K'):
      temp_df = {'metric': 'LTM Revenue', 'value': max(master_dict['Revenues'][x]) , 'formula': 'Revenues','base_dependencies':format_base_dep([('us-gaap:Revenues',x)]),'filing_date': x,'form_type':master_dict1['Revenues'][x]['form_type'] ,'cik':master_dict1['Revenues'][x]['cik'],'accession_number':master_dict1['Revenues'][x]['accession_number']}
      output_df = output_df.append(temp_df, ignore_index=True)
    
   
  """
  Growth Persistence=(current quarter revenue(us-gaap:Revenues or us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax) - previous year same quarter revenue(us-gaap:Revenues or us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax))/(previous year same quarter revenue) (us-gaap:Revenues or us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax)
  """
  union_set = set().union(*[master_dict['RevenueFromContractWithCustomerExcludingAssessedTax'], master_dict['Revenues']])
  union=sorted(union_set)
  references=[]
  # print(union)
  for i in range(len(union)-1, -1, -1):
    curr_quarter=union[i]
    for j in range(i-1,-1, -1):
      if((curr_quarter-union[j]).days< 405 and (curr_quarter-union[j]).days>325):
        prev_quarter=union[j]
        if(union[j] in master_dict['RevenueFromContractWithCustomerExcludingAssessedTax'] and master_dict1['RevenueFromContractWithCustomerExcludingAssessedTax'][union[j]]['form_type']=="10-Q" and curr_quarter in master_dict['RevenueFromContractWithCustomerExcludingAssessedTax'] and master_dict1['RevenueFromContractWithCustomerExcludingAssessedTax'][curr_quarter]['form_type']=="10-Q"):
          pers=(max(master_dict['RevenueFromContractWithCustomerExcludingAssessedTax'][curr_quarter])-max(master_dict['RevenueFromContractWithCustomerExcludingAssessedTax'][prev_quarter]))/max(master_dict['RevenueFromContractWithCustomerExcludingAssessedTax'][prev_quarter])
          temp_df = {'metric': 'Growth Persistence', 'value': pers , 'formula': 'current quarter revenue - previous year same quarter revenue /previous year same quarter revenue','base_dependencies':format_base_dep([('us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax',union[i])]),'filing_date': union[i],'form_type':master_dict1['RevenueFromContractWithCustomerExcludingAssessedTax'][union[i]]['form_type'] ,'cik':master_dict1['RevenueFromContractWithCustomerExcludingAssessedTax'][union[i]]['cik'],'accession_number':master_dict1['RevenueFromContractWithCustomerExcludingAssessedTax'][union[i]]['accession_number']}
          output_df = output_df.append(temp_df, ignore_index=True)
          break
        elif(union[j] in master_dict['Revenues'] and master_dict1['Revenues'][union[j]]['form_type']=="10-Q" and curr_quarter in master_dict['Revenues'] and master_dict1['Revenues'][curr_quarter]['form_type']=="10-Q"):
          pers=(max(master_dict['Revenues'][curr_quarter])-max(master_dict['Revenues'][prev_quarter]))/max(master_dict['Revenues'][prev_quarter])
          temp_df = {'metric': 'Growth Persistence', 'value': pers , 'formula': 'current quarter revenue-previous year same quarter revenue /previous year same quarter revenue','base_dependencies':format_base_dep([('us-gaap:Revenues',union[i])]),'filing_date': union[i],'form_type':master_dict1['Revenues'][union[i]]['form_type'] ,'cik':master_dict1['Revenues'][union[i]]['cik'],'accession_number':master_dict1['Revenues'][union[i]]['accession_number']}
          output_df = output_df.append(temp_df, ignore_index=True)
          break
          

  """
  Last Year Quarter Growth= Get the revenues from the last two year 10Q filing excluding the latest filing and divide these values
  """
  union_set = set().union(*[master_dict['RevenueFromContractWithCustomerExcludingAssessedTax'], master_dict['Revenues']])
  union=sorted(union_set)
  references=[]

  for i in range(len(union)-1, -1, -1):
    # print(master_dict1['RevenueFromContractWithCustomerExcludingAssessedTax'][union[i]]['form_type'])
    found=False     
    lyqg = None 
    if (union[i] in master_dict1['RevenueFromContractWithCustomerExcludingAssessedTax'] and master_dict1['RevenueFromContractWithCustomerExcludingAssessedTax'][union[i]]['form_type']=="10-Q") or (union[i] in master_dict['Revenues'] and master_dict1['Revenues'][union[i]]['form_type']=="10-Q"):
      curr_quarter=union[i]
      for j in range(i-1,-1, -1):
        if((curr_quarter-union[j]).days< 405 and (curr_quarter-union[j]).days>325):
          prev_quarter1=union[j]
          found=False
          for k in range(j-1,-1, -1):
            if((curr_quarter-union[k]).days< 800 and (curr_quarter-union[k]).days>600):
              prev_quarter2=union[k]
              if(prev_quarter1 in master_dict['RevenueFromContractWithCustomerExcludingAssessedTax'] and prev_quarter2 in master_dict['RevenueFromContractWithCustomerExcludingAssessedTax']):
                lyqg=max(master_dict['RevenueFromContractWithCustomerExcludingAssessedTax'][prev_quarter1])/max(master_dict['RevenueFromContractWithCustomerExcludingAssessedTax'][prev_quarter2])
                acc_no = master_dict1['RevenueFromContractWithCustomerExcludingAssessedTax'][union[i]]['accession_number'] if union[i] in master_dict1['RevenueFromContractWithCustomerExcludingAssessedTax'] else master_dict1['Revenues'][union[i]]['accession_number']
                temp_df = {'metric': 'Last Year Quarter Growth', 'value': lyqg , 'formula': 'previous year same quarter revenue/last 2 year same quarter revenue','base_dependencies':format_base_dep([('us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax',prev_quarter1), ('us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax',prev_quarter2)]),'filing_date': union[i],'form_type':"10-Q" ,'cik':master_dict1['RevenueFromContractWithCustomerExcludingAssessedTax'][prev_quarter1]['cik'],'accession_number':acc_no}
                output_df = output_df.append(temp_df, ignore_index=True)
                found=True
                break
              elif(prev_quarter1 in master_dict['Revenues'] and prev_quarter2 in master_dict['Revenues']):
                lyqg=max(master_dict['Revenues'][prev_quarter1])/max(master_dict['Revenues'][prev_quarter2])
                acc_no = master_dict1['RevenueFromContractWithCustomerExcludingAssessedTax'][union[i]]['accession_number'] if union[i] in master_dict1['RevenueFromContractWithCustomerExcludingAssessedTax'] else master_dict1['Revenues'][union[i]]['accession_number']
                temp_df = {'metric': 'Last Year Quarter Growth', 'value': lyqg , 'formula': 'previous year same quarter revenue/last 2 year same quarter revenue','base_dependencies':format_base_dep([('us-gaap:Revenues',prev_quarter1), ('us-gaap:Revenues',prev_quarter2)]),'filing_date': union[i],'form_type':"10-Q" ,'cik':master_dict1['Revenues'][prev_quarter1]['cik'],'accession_number':acc_no}
                output_df = output_df.append(temp_df, ignore_index=True)
                found=True
                break
        if(found):
          break


  """
  Last Year Run Rate Revenue = Last year quarter revenue * 4
  =us-gaap:Revenues * 4  or (us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax)*4
  """
  
  
  # """
  # Implied Net New ARR ==(us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax or us-gaap:Revenues (latest quarter) - us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax or us-gaap:Revenues (previous quarter))*4
  #  """
  # union1 = set().union(*[master_dict['RevenueFromContractWithCustomerExcludingAssessedTax'], master_dict['Revenues']])
  # #union1=list(union1)
  # print(union1)
  # intersection=[]
  # for i in range (len(union1)):
  #   intersection.append(max(master_dict['RevenueFromContractWithCustomerExcludingAssessedTax'][union1[x]],master_dict['Revenues'][union1[x]]))
  
  # intersection=list(intersection)
  # sorted_dict=sorted(intersection,reverse=True)
  # l=len(sorted_dict)
  # i=0
  # sorted_list = [(k, v) for k, v in sorted_dict.items()]
  # for x in sorted_list:
  #   if(master_dict1['RevenueFromContractWithCustomerExcludingAssessedTax'][x[0]]=='10-Q'or master_dict1['Revenues'][x[0]]=='10-Q' ):
  #     if(i+1<l):
  #       if(master_dict1['RevenueFromContractWithCustomerExcludingAssessedTax'][sorted_list[i+1][0]]=='10-Q'and master_dict1['Revenues'][sorted_list[i+1][0]]=='10-Q' and (sorted_list[i][0]-sorted_list[i+1][0]).days<=120 ):
  #         result=(x[1]-sorted_list[i+1][1])*4
  #         temp_df = {'metric': 'Implied Net New ARR', 'value': result , 'formula': '(us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax or us-gaap:Revenues (latest quarter) - us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax or us-gaap:Revenues (previous quarter))*4','filing_date': x,'form_type':master_dict1['DepreciationDepletionAndAmortization'][x]['form_type'] ,'cik':master_dict1['DepreciationDepletionAndAmortization'][x]['cik'],'accession_number':master_dict1['DepreciationDepletionAndAmortization'][x]['accession_number']}
  #         output_df = output_df.append(temp_df, ignore_index=True)
  #       else:
  #         sum=0
  #         if(sorted_list[i][0]-sorted_list[i+1][0]<=120):
  #           for k in range (3):
  #             if(i+k+2<l and master_dict1['RevenueFromContractWithCustomerExcludingAssessedTax'][sorted_list[i+k+2][0]]=='10-Q'and master_dict1['Revenues'][sorted_list[i+k+2][0]]=='10-Q' and (sorted_list[i+1][0]-sorted_list[i+2+k][0]).days<=365 ):
  #               sum+=sorted_list[i+2+k][1]
  #             if k==3:
  #               result=(x[1]+sum-sorted_list[i+1][1])*4
  #               temp_df = {'metric': 'Implied Net New ARR', 'value': result , 'formula': '(us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax or us-gaap:Revenues (latest quarter) - us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax or us-gaap:Revenues (previous quarter))*4','filing_date': x,'form_type':master_dict1['DepreciationDepletionAndAmortization'][x]['form_type'] ,'cik':master_dict1['DepreciationDepletionAndAmortization'][x]['cik'],'accession_number':master_dict1['DepreciationDepletionAndAmortization'][x]['accession_number']}
  #               output_df = output_df.append(temp_df, ignore_index=True)
            
  #   elif (master_dict1['RevenueFromContractWithCustomerExcludingAssessedTax'][x[0]]=='10-K'or master_dict1['Revenues'][x[0]]=='10-K' ):
  #     sum=0
  #     for k in range (3):
  #       if(i+k+1<l and (master_dict1['RevenueFromContractWithCustomerExcludingAssessedTax'][sorted_list[i+k+1][0]]=='10-Q'or master_dict1['Revenues'][sorted_list[i+k+1][0]]=='10-Q') and (sorted_list[i][0]-sorted_list[i+1+k][0]).days<=365 ):
  #         sum+=sorted_list[i+1+k][1]
  #     if k==3:
  #       result=(x[1]-sum-sorted_list[i+1][1])*4
  #       temp_df = {'metric': 'Implied Net New ARR', 'value': result , 'formula': '(us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax or us-gaap:Revenues (latest quarter) - us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax or us-gaap:Revenues (previous quarter))*4','filing_date': x,'form_type':master_dict1['DepreciationDepletionAndAmortization'][x]['form_type'] ,'cik':master_dict1['DepreciationDepletionAndAmortization'][x]['cik'],'accession_number':master_dict1['DepreciationDepletionAndAmortization'][x]['accession_number']}
  #       output_df = output_df.append(temp_df, ignore_index=True)
  #   i+=1

  # rfc = [ (x, max(master_dict['RevenueFromContractWithCustomerExcludingAssessedTax'][x])) for x in sorted(master_dict['RevenueFromContractWithCustomerExcludingAssessedTax'])]
  # rev = [ (x, max(master_dict['Revenues'][x])) for x in sorted(master_dict['Revenues'])]
  
  # for i in range(len(rfc)-1, 0, -1):
  #   # check if the date diff is correct
  #   print(rfc[i][0]-rfc[i-1][0])
  #   if(rfc[i][0]-rfc[i-1][0] < datetime.timedelta(days=120)):
  #     temp_df = {'metric': 'Implied Net New ARR', 'value': rfc[i][1]-rfc[i-1][1] , 'formula': 'RevenueFromContractWithCustomerExcludingAssessedTax(current quarter) - (us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax(last quarter)','filing_date': rfc[i][0]}
  #     output_df = output_df.append(temp_df, ignore_index=True)
  # display(output_df)
  return output_df


i=0
for cik, df in data.groupby(['CIK']):
  new_df=metric_calculation(df)
  new_df.to_csv(OUTPUT_BASE_PATH+str(cik)+'.csv')
  i=i+1


# len(os.listdir(OUTPUT_BASE_PATH))

print("Extracted all metrics and stored.")

