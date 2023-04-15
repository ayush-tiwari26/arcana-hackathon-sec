import psycopg2
import psycopg2.extras as extras
import numpy as np
import requests 
import os
import json
import pandas as pd
from datetime import date


ID_CIK_MAPPING_CSV = os.path.expanduser('~/sec-scraper/data/input_data/company_cik_to_id.csv')
BASE_METRICS_BASEPATH = os.path.expanduser('~/sec-scraper/data/parsed_data/xbrl/{}/'.format(date.today()))


 
if not os.path.exists(BASE_METRICS_BASEPATH):
    os.makedirs(BASE_METRICS_BASEPATH)

###################################
# Create cursor for connection to DB
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

df_id = pd.read_csv(ID_CIK_MAPPING_CSV)


def pushToDB(df):

    tuples = [tuple(x) for x in df.to_numpy()]
  
    cols = ','.join(list(df.columns))
    query = "INSERT INTO dashboard_api_basemetrics (%s) VALUES %%s" % (cols)

    try:
        extras.execute_values(cursor, query, tuples)
        connection.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        connection.rollback()
    

# debug statement
i=0;

for file in os.listdir(BASE_METRICS_BASEPATH):
	df = pd.read_csv(BASE_METRICS_BASEPATH + file)

	print("Pushing base metrics from file: {} ...".format(file))
	df = df.iloc[: , 1:]	
	name_dict = {
	'xbrl_tag_name':'tag',
	"CIK":"company_id",
	"accession_no":"accession_no",
	"unitref":"unit",
	"FilingDate":"filing_date",
	"FormType"	:"form_type",
	"value"	: "value",
	"source": "source" 
	}
	df.rename(columns = name_dict, inplace = True)
	df['value']=df['value'].apply ( lambda x: x.replace(',',''))
	
    # uncomment this and remove below statement in production
	df["company_id"] = df["company_id"].replace(df_id["cik"].values.tolist(),df_id["id"].values.tolist())
	df["decimel"] = ""

	pushToDB(df)
	i+=1


cursor.close()
