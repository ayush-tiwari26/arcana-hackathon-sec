source ~/sec-scraper/xbrl-scrapper/xbrl_env/bin/activate
/home/ubuntu/sec-scraper/xbrl-scrapper/xbrl_env/bin/python ~/sec-scraper/xbrl-scrapper/test_parse.py

/home/ubuntu/sec-scraper/xbrl-scrapper/xbrl_env/bin/python ~/sec-scraper/xbrl-scrapper/push_metrics.py

/home/ubuntu/sec-scraper/xbrl-scrapper/xbrl_env/bin/python -W ignore ~/sec-scraper/xbrl-scrapper/extract_metrics.py
/home/ubuntu/sec-scraper/xbrl-scrapper/xbrl_env/bin/python ~/sec-scraper/xbrl-scrapper/push_derived.py
