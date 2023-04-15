# SaaSiFi Documentation (Team 5)
**Live Dashboard link** -  https://saasifi.in/ <br>
**API Endpoint** -  https://api.saasifi.in/

![](https://i.ibb.co/f9270LV/AWS-Networking-1.png)

The figure above shows the scalable architecture of SaaSiFi. Standard practices have been followed for hosting frameworks and database. Along with the dashboard visualizations, we implemented an AWS Lambda triggered automated pipeline to scrape any newly published SEC filing, calculate the metrics and push to our database using AWS Lambda and notify a selected set of users using AWS SNS. More details regarding each of the section is given below. 

## Submission Files Overview
There are a total of 3 repositories (or folders in the submission), namely:
-   `frontend` - contains the code for the frontend for the dashboard
-   `backend` - contains the code for REST API backend framework
-   `sec-scrapers` - contains the code for AWS lambda automation and notification pipeline to scrape the new SEC filings periodically, along with the scripts for data-preprocessing, information and metrics extraction, risk analysis, sentiment analysis and financial sheets extraction. The folder also serves as a collection of all the various NLP approaches implemented.

*Note - The documentation below only describes the file organization and details of the API and execution of the submitted scripts. More details on the  different models and approaches used for automation, NLP and IR techniques is provided with the report*

## frontend
React has been used for SaaSiFi frontend, along with TypeScript. TypeScript enables us to write quality code in which chances of error are reduced before being pushed to production.

We have used `styled-components` for styling, and `@nivo/bar` for making canvas charts which are robust for large datasets. To setup this locally, follow `README.md` under `frontend/`


## backend
Backend is implemented using the [Django REST framework](https://www.django-rest-framework.org/).  A single app `dashboard_api` implements all the required APIs, the structure of which is provided below:

    ├── dashboard_api
    │   ├── admin.py
    │   ├── apps.py
    │   ├── db_populate
    │   │   ├── basepopulate.py
    │   │   ├── derivedpopulate.py
    │   │   ├── companypopulate.py
    │   │   ├── metricpopulate.py
    │   │   ├── sentimentpopulate.py
    │   │   ├── textderivedpopulate.py
    │   ├── migrations
    │   ├── models.py
    │   ├── serializers.py
    │   ├── tests.py
    │   ├── urls.py
    │   ├── views.py

Most of the files are globally used standard files for Django. Relevant additional information to this is provided below:
* Backend is hosted on [Amazon Elastic Compute Cloud](https://aws.amazon.com/ec2/) on a `r6i.xlarge` type instance 
* [PostgreSQL](https://www.postgresql.org/) is used for database, deployed on [Amazon RDS](https://aws.amazon.com/rds/postgresql/) 
*   `db_populate/` - contains the scripts used to bulk update the extracted data to the cloud database
* Metrics taxonomy - **Base metrics** are the ones extracted directly from the filings. **Derived metrics** are the ones derived from base metrics via some calculation. Eg. Debt and Equity are base metrics, while Debt to Equity ratio is a derived metric
* To avoid processing overhead expenses during the navigation of our dynamic website, caching is implemented 
* To setup backend development server locally, follow `README.md` under `backend/`

*Details of the APIs are mentioned at the bottom of the documentation.*

## sec-scrapers
The ultimate goal of the sec-scraper is to provide a real-time update on the dashboard whenever a new filing is added to the SEC EDGAR portal. We use [AWS Lambda](https://aws.amazon.com/lambda/), which is a serverless, event-driven compute service to identify the newly added filings which are not yet present in the SaaSiFi's database. More details regarding the process is provided alongwith the file organization:

    ├── sec-scraper/
    │   ├── xbrl-scraper/
    │   │   ├──  ------
    │   ├── filings-scraper/
    │   │   ├──  ------
    │   ├── table-scraper/
    │   │   ├──  ------
    │   ├── text-based-metrics-extraction/
    │   │   ├──  ------
    │   ├── sentiment-analysis/
    │   │   ├──  ------
    │   ├── others/
    │   │   ├──  ------
    │   ├── data/
    │   │   ├──  ------
    │   ├── ec2_trigger_lambda/
    │   │   ├──  --------

### AWS Lambda function to trigger SEC filings `ec2_trigger_lambda/` 

We have implemented an AWS lambda function that is triggered daily at 6:00 AM UTC and then turns on a worker EC2 instance which sequentially runs the pipeline for extracting and parsing new filings which have been added to the EDGAR  database during the day. There are many architectural benefits that make scheduled lambda functions a better choice:

It allows us to flexibly target different EC2 instances (or a subset of the given instances) by abstracting job scheduling. This allows us to scale the worker environments to multiples instances in the future. Since AWS Lambda is serverless, we do not need to keep our worker instances switched on all the time saving us compute and consequently money.

After the metrics have been extracted by the worker instances of EC2, the details of the newly extracted filings are then published to the SNS Topic which in turn sends a notification to all the subscribed users. 

### Automation to update new SEC filings `xbrl-scrapper/` 

The EDGAR Database is updated daily with new filings after 5:30P.M ET. To update our database with these new filings an AWS lambda is triggered everyday at 6 AM UTC. It verifies if the EC2 machine is on/off, and turns it on if required, followed by the execution of `script.sh`   	 	

     ├── xbrl-scraper
    	│   ├── pysecxbrl/
    	│   ├── script.sh
    	│   ├── extract_metrics.py
    	│   ├── push_derived.py    
    	│   ├── push_metrics.py
    	│   ├── test_parse.py

* `script.sh` - This script will be triggered by AWS Lambda. It executes the remaining scripts to check for a new SEC filing and to calculate metrics, update metrics and notify the user if found any. Notification of any new filing is published to all subscribers using [AWS SNS topic](https://aws.amazon.com/sns/?whats-new-cards.sort-by=item.additionalFields.postDateTime&whats-new-cards.sort-order=desc)
* `test_parse.py` - For each CIK, it fetches the available filings and connects to our cloud database to check if filing is in database. If any new filing is detected, it stores the base metrics of the filings. It requires a company vs cik mapping `cik_sheet1.csv`
* `push_metrics.py` - Pushes the base metrics obtained for the newly added SEC filing to the database
* `extract_metrics.py` - Calculates the derived metrics for newly obtained SEC filings. It requires a `master.csv` to calculate the metrics which are dependent on the previous filings data.
* `push_derived.py`- Pushes the derived metrics obtained for the newly added SEC filing to the database


### Forms extraction pipeline `filings-scraper/`

This folder contains python files to scrape 10-K,10-Q and 8-K forms from the sec.gov website. We can crawl and download financial reports for each publicly-traded company, for specified years, through the  `edgar_crawler.py`  module. 
 We have used beautiful soup library in python for the implementation. Other major queries are passed through `config.json` file, which allows to select quarters and starting and ending of filing years of our choice. 


      ├── filing-scraper
            ├── config.json
    		├── datasets
    		│   └── companies_info.json
    		├── edgar_crawler.py
    		├── extract_items_10k.py
    		├── extract_items_10q.py
    		├── extract_items_8k.py
    		└── requirements.txt
* `config.json` is used to provide arguments for `edgar_crawler.py`, the module to download financial reports
*  `edgar_crawler.py` is used extract and clean specific text sections, such as Risk Factors, MD&A, and others, it is done through the  `extract_items.py`  module. CIK Numbers are given using  `CIK.csv`  and  `edgar_crawler.py`  to generate all the filings for the given cik numbers and duration.
* `extract_items_10k.py`  is used to extract all the 10k forms 
*  `extract_items_10q.py`  is used extract all the 10q forms
*   `extract_items_8k.py`  is used to extract all the 8k forms

### NLP approaches to extract metrics from text and tables `text-based-metrics-extraction/`
This folder contains the notebooks related to the natural language processing pipeline. The natural language processing pipeline mainly deals with the extraction of metrics and their values on specific dates from the unstructured text extracted from `10K filings` and stored in the form of `JSON`.
	
     ├── text-based-metrics-extraction
    	│   ├── NLP_Pipeline.ipynb
    	│   ├── NER_Dependency_Tree.ipynb
    	│   ├── files
    	|   |   ├── metrics.json
    	│   ├── sample-10K
    	|   |   ├── 10K-(...).json
* `NLP_Pipeline.ipynb` - This file contains the notebook having  the code for extracting metrics, values and dates from the extracted `10K filings`
  * This notebook refers to the custom metrics list stored in `./files/metrics.json` 
  * Make sure you have live internet connection while running the notebook, since the Question Answering and NER models will be downloaded from `huggingface-hub` and `spacy-hub` respectively
  * This Notebook contains `four` main modules, which have separate functioning as per use cases
  	* ***Entity Recognition Module*** - This module contains the logic of recognizing the relevant entities and cleaning the answer returned. This module makes use of the `en_core_web_lg` model for NER task.
  	*  ***Question Answering Module*** - This module contains the logic for creating right questions for extracting relevant answers relating to the metrics from the context.
  	* ***Sentence Extraction Module*** - This module has the utility functions that will be used to extract metrics present in a single sentence. This module inherits the utility functions from `Entity Recognition Module` and `Question Answering Module` to achieve the task of extracting metric.
  	* ***Paragraph Extraction Module*** - This module makes use of the `Sentence Extraction Module` to extract the metrics from each sentence in the paragraph. This module also has some optimization logic implemented for fast extraction of metric from a big paragraph.
  	* ***Float Conversion Pipeline*** - Once the above phases have been completed by the model, we see that sometimes the extracted values may not have proper boundaries on the number (Eg. $1 may be extracted as `was $1`) and it is important to convert the `numbers from text` to `floating point values` to facilitate further processing (Eg.  two dollars sixty cents should be converted to 2.60). Hence we make use of the ***word2number*** library along with our algorithmic pipeline to convert the values extracted to floating point numbers.
  * For executing this file, the user needs to set the following _variables_ in the notebook under the JSON testing section.
```
FILINGS_PATH = 'path/to/filings-10K' # Path to the folder containing 10K filings
OUTPUT_PATH = 'path/to/output'       # Path to the output folder
```
* `NER_Dependency_Tree.ipynb` -  This notebook contains the code for testing dependency parser based tree approach to link the metrics, dates and values. 
  * The notebook makes use of the `en_core_web_lg` model that is available on the `SpaCy-hub`
  * Tree is visualized using the the python `treelib` library, and we get easy to comprehend visualization as follows
* `Sample-10K` - This folder contains sample extracted 10K filings  that can be used for testing the NLP pipeline for working.
```
was
├── .
├── ARR
│   ├── Creative
│   └── for
│       └── DATE-0
├── MONEY-1
├── and
└── was
    ├── MONEY-2
    └── for
        └── DATE-3
```
* `files/metrics.json` - This file contains carefully curated metrics list that is relevant from financial perspective and can be extracted from SEC filings.
  * This list can be replace with the custom list of the user, if they choose to.
  * The `metrics.json` file is referred in the `NLP_Pipeline` notebook while extracting the metrics from the respective sentences.
  )

### Sentiment Extraction `sentiment-analysis/`
This folder contains entire sentiment analysis pipeline that was used for making the predictions on the `item 7 and item 9` of the 10K reports. It includes the code used for the baseline model (Bi-LSTM model) as well as the other three models used for sentiment analysis.
	
     ├── sentiment-analysis
    	│   ├── NLP BiLSTM model.ipynb
    	│   ├── NLP Sentiment Analysis Pipeline.ipynb
    	│   ├── Benchmark.ipynb
    	│   ├── sentiment-model
    	│   ├── benchmark.csv

* `NLP BiLSTM model.ipynb` - This file contains the code to fine tune Bi-LSTM model on financial phrases dataset. We used an [EDGAR-W2V](https://arxiv.org/abs/2109.14394) embedding model for getting word vectors along with the Bi-LSTM architecture. The model is trained on [financial Phrasebank dataset](https://arxiv.org/pdf/1307.5336.pdf)
* `NLP Sentiment Analysis Pipeline.ipynb` - This file contains the pipeline implemented for performing sentiment analysis on the 10K reports. We used voting between three different versions of [finBERT](https://arxiv.org/abs/1908.10063), [financialBERT](https://www.researchgate.net/publication/358284785_FinancialBERT_-_A_Pretrained_Language_Model_for_Financial_Text_Mining) and finetuned [DistillroBERTa](https://arxiv.org/abs/1910.01108) model in order to get the sentiment predictions of text. 
* `Sentiment model` - This directory contains the saved weights for `Bi-LSTM` model that has been trained using the  [EDGAR-W2V](https://arxiv.org/abs/2109.14394) word embeddings. This model will be loaded in the `Benchmark.ipynb` to create the results for the benchmark test file. Two sample json text files which were given as input and their corresponding predictions are also added in the folder.
* `Benchmark.ipynb` - This file contains the benchmarking script for all the 5 models that have been tested. For `AWS comprehend`, user must set the Access Key, Secret Access Key and Region using `aws-cli`. Apart from this set the `BENCHMARK_FILE_PATH` variable in the `Benchmark.ipynb` file which contains the required sentences in `Text` column and the ground truth sentiments in the `Sentiment` column. Output of the evaluation is saved in `eval.csv` file in the current working directory.  
* `benchmark.csv` - An example benchmark file which has been annotated by a group of professionals. The sentences are selected from variety of SEC filings of different companies and from different items too. This `benchmark.csv` file can be directly imported in `Benchmark.ipynb` to generate the below achieved results.

Several paid APIs are also available for sentiment analysis, like [AWS Comprehend](https://aws.amazon.com/comprehend/), but are not feasible for large volumes of data. AWS Comprehend charges **~1 USD** per `item 7`.  For benchmarking the results, we extract and annotate 200 random sentences from `item 7` of the 10-K filings, and report the accuracy, precision, recall and F1 score on all four models, along with the AWS Comprehend sentiment analysis pipeline. Results are reported below
| model | Accuracy | Precision | Recall | F1 Score |
| ---  | ---  | --- | --- | --- | 
| FinBERT | 0.839196 | 0.835362 | 0.841359 | 0.830182 |
| FinancialBERT | 0.78392 | 0.782894 | 0.765152 | 0.77392164 |
| DistilRoBERTa_finetuned | 0.788945 | 0.774713 | 0.750205 | 0.762262 |
| AWS Comprehend | 0.386935 | 0.792517 | 0.349918 | 0.485482 |
| BiLSTM + CNN | 0.628141 | 0.561235 | 0.546581 | 0.553811 | and [DistillroBERTa](https://arxiv.org/abs/1910.01108) model in order to get the sentiment predictions of text.

### Risk analysis and MD&A  heatmap analysis `others/`
This folder contains the code used for other tasks such as, word count, bigram and trigram count and obtaining a check on risk analysis of the 10-K filing. It also has the code required for other useful analysis like risk sentiments. 
	
     ├── other
    	│   ├── NLP word_count_Pipeline.ipynb
    	│   ├── risk.ipynb
    	│   ├── files
    	|   |   ├── risks.txt 

* `NLP word_count_Pipeline.ipynb` - This file contains the code for word count extraction, bigram and trigram frequency count  text analysis of t.
* `risk.ipynb` - This notebook contains the code to create the risk sentiment scores for the given SEC filings. The notebooks requires SEC filings stored in a directory and we need to set the following variables to generate the sentiment scores from `risk.ipynb`
```
risks_file_path = '/path/to/risks.csv' # Path to the risks wordlist file
filings_path_10K = '/path/to/10-K/'    # Path to the folder containing 10-K files
```
* `files/risks.txt` - This file contains the wordlist and the category of the risks they belong to. This file will be used to generate the risk sentiment scores in `risk.ipynb` notebook.

*Reference Article*
Campbell, J.L., Chen, H., Dhaliwal, D.S. _et al._  
The information content of mandatory risk factor disclosures in corporate filings.
 _Rev Account Stud_  **19,** 396–455 (2014). https://doi.org/10.1007/s11142-013-9258-3` - 

## API Documentation

| Type | API  | Description | Input parameters | Sample Output |
|---|--|------------------|----|--|
| GET | `/companies` | To get the mapping of all company names versus the cik|| {<br>"DOCUSIGN, INC.":"1261333",<br>"Dynatrace, Inc.":  "1773383"<br>} |
|  GET  | `/companies_list` | Get details of a company from it's CIK | cik | [<br>{<br>"cik":  "8670",<br>"name":  "AUTOMATIC DATA PROCESSING INC",<br>"ticker":  "['ADP']",<br>"website":  "",<br>"addresses":  "",<br>"phone":  "9739745000",<br>"sic":  "7374",<br>"category":  "Large accelerated filer",<br>"overview":  "Automatic Data Processing, Inc. (ADP) is an American provider of human resources management software and services.",<br>"founding_year":  "1949",<br>"state_of_incorporation":  "DE <br>}<br>]|
| GET| `/base_metrics`| To get the list of base metrics that are extracted directly from filings. Some of the extracted metrics include : Assets Current, Revenues, Liabilities.<br>|cik<br>tag<br>form_type<br>start_date<br>end_date   | [<br>{<br>"tag": "us-gaap:NetIncomeLoss",<br> "company": 196,<br> "value": -5323.0, <br>"decimel": "",<br> "unit": "USD",<br> "form_type": "10-Q",<br> "accession_no": "0001493152-21-011278", <br>"filing_date": "2021-05-13", <br>"source": "xbrl"<br>}<br>]|
| GET | `/derived_metrics` | To get the list of derived metrics which are calculated using the base metrics that are extracted directly from filings. Some of the calculated  metrics include : ARRR, NTM-ARRR| cik<br>tag<br>form_type<br>start_date<br>end_date|[<br>{<br>"company": 224,<br> "tag": "Annualized Revenue Run Rate (ARRR)", <br>"value": 3143080000.0,<br> "formula": "RevenueFromContractWithCustomerExcludingAssessedTax*4", <br>"description": "This measures the annualized revenue from quarterly revenue.", <br>"filing_date": "2022-01-31", <br>"accession_no": "0000008670-22-000014",<br> "unit": "",<br> "form_type": "10-Q",<br> "source": "xbrl", <br>"sentence": "", "score": 0.0 <br>}<br>]|
| GET | `/yahoo_finance` |To get the details of stock prices, market gap and ,to calculate EV metrics. The stock prices and other relevant data are obtained from Yahoo finance and calculated derived metrics |cik| {<br>"tag": ["Multiple on End of First Day IPO Price",<br>"Multiple on IPO Price",<br>"Share price",<br> "Percent of 52 week high",<br> "Market Cap",<br>"value": [259.7796448647771, 89079000000.0<br>89079000000.0],<br> "prevpresent": [1, 1, 1, 0, 0, 1, 0, 1, 1], <br>"prevvalue": [259.5962252853177, 259.5962252853177, 212.30999755859375, "", "", 92944780000.0, "", 63.705314671894065, 15.926328667973516]<br>}|
| GET | `/share_price` | To plot the trend of the share prices of a company | cik |{<br>"date_list": ["2017-01-03T00:00:00",....]<br>"price_list": [103.5,103.66000366210938]<br>}|
| GET | `/balancesheet`| To get the balance sheet, statements of income and cash flow of a specified company| cik |{<br><Table: Consolidated Balance Sheets><br><Table: Consolidated Statements of Incomes><br>}  |
| GET | `/heat_map` | To get the heat map of frequency of selected words in a particular company's filing| cik |{<br>"id": "absence", <br>"data": [<br>{"x": "16", "y": 1.0}, {"x": "17", "y": 1.0}, {"x": "18", "y": 1.0}, {"x": "19", "y": 1.0}, {"x": "20", "y": 2.0}, {"x": "21", "y": 2.0}<br>]<br>}|
| GET | `/sentiment` | To get the sentiments of extracted textual data from various sections of filings of a particular company|cik |"item": ["item_7", "item_7A"],<br> "filing_date": ["2021-06-30", "2021-06-30"],<br> "confidence": [0.9723022361509664, 0.9998824596405028],<br> "label": ["neutral", "neutral"],<br> "positive": ["[[6279, 6398]]", "[[7445, 7601]]"],<br> "negative": ["[[12329, 12647], [42954, 43074]]"]|
| GET | `/risk_metric` | Returns the risk sentiment score categorized in financial,otheridiosyncracies,legal,othersystematic and tax | cik |{<br>"year": ["2019", "2020", "2021"],<br> "financial": [7.442943495848727, 7.832890014164741, 7.8703647195834066],<br> "otheridiosyncracies": [11.411510988012074, 11.558420713268664, 11.653292945382814],<br> "legal": [8.63662462054365, 8.707359132080883, 8.714245517666122],<br> "othersystematic": [9.52552080909507, 9.722807531169547, 9.771489469500601],<br> "tax": [7.584962500721158, 7.614709844115207, 7.562242424221072]},|
| GET | `/unique_metrics` |Returns all the metrices available for a particular company| cik |{<br>"tags": ["EBITDA"]<br>}|
| GET | `/ownership` | To get direct holders and institutional holders of a particular company. | cik |{<br>"Direct Holders": <br>[{"Holder": "Vanguard Group, Inc. (The)",<br> "Shares": 38433923,<br> "Date Reported": "Dec 30, 2021",<br> "% Out": "8.14%",<br> "Value": 21794340376}]<br>}|
| GET | `/benchmarking` | To compare derived metrics of given companies year wise.|list of ciks |["debt to equity":<br> [<br>{"year": "2017",<br>"8670": 0.684,<br>"796343": 0},<br>{"year": "2018",<br>"8670": 772.6,<br>"796343": 0},<br>{"year": "2019",<br>"8670": 33.6,<br>"796343": 43.89}<br>]<br>]|
