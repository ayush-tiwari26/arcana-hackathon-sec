import psycopg2
import psycopg2.extras as extras
import numpy as np
import requests 
import os
import json
import pandas as pd
from datetime import date



ID_CIK_MAPPING_CSV = os.path.expanduser('~/sec-scraper/data/input_data/company_cik_to_id.csv')
EXTRACTED_METRICS_BASEPATH = os.path.expanduser('~/sec-scraper/data/parsed_data/xbrl/metrics/derived_metrics/')

 
if not os.path.exists(EXTRACTED_METRICS_BASEPATH):
    os.makedirs(EXTRACTED_METRICS_BASEPATH)

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

def checkFilingExists(accession_no):

    global cursor
    query = """SELECT * FROM dashboard_api_derivedmetrics WHERE accession_no='{}'""".format(accession_no)
    try:
        cursor.execute(query)
        record = cursor.fetchall()
    except:
        print("cannot access DB")
        return
    if(len(record) == 0):
        return False
    return True

def pushToDB(df):

  
    tuples = []

    for x in df.to_numpy():
        if(checkFilingExists(x[6]) == False):
            # print("{} : does not exist".format(x[6]))
            tuples.append(x)
    if(len(tuples) == 0):
        return

    cols = ','.join(list(df.columns))

    query = "INSERT INTO dashboard_api_derivedmetrics (%s) VALUES %%s" % (cols)

    try:
        extras.execute_values(cursor, query, tuples)
        connection.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        connection.rollback()
    

# debug statement
i=0;

for file in os.listdir(EXTRACTED_METRICS_BASEPATH):
    df = pd.read_csv(EXTRACTED_METRICS_BASEPATH + file)

    df = df.iloc[: , 1:]
    if('base_dependencies' in df.columns):
        df = df.drop("base_dependencies", axis=1)
    print("Pushing derived metrics from file: {} ...".format(file))
    
    name_dict = {
    'metric':'tag',
    "cik":"company_id",
    "accession_number":"accession_no",
    "value" : "value",
    "form_type" :"form_type",
    "filing_date":"filing_date",
    "formula":"formula"
    }
    df.rename(columns = name_dict, inplace = True)
    
    # uncomment this and remove below statement in production
    df["company_id"] = df["company_id"].replace(df_id["cik"].values.tolist(),df_id["id"].values.tolist())
    df["source"] = "xbrl"
    df["unit"] = df["description"]  = df["sentence"] = df["sentence_date"] = ""
    df["score"]  = 0

    pushToDB(df)
    i+=1


cursor.close()
