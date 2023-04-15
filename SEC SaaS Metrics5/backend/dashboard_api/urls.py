import re
from django.urls import re_path
from rest_framework.urlpatterns import format_suffix_patterns
from dashboard_api import views 
 
urlpatterns = [ 
    re_path(r'companies_list$', views.companies_list),
    re_path(r'companies/$', views.company_details),
    re_path(r'base_metrics/$', views.base_metrics_list),   
    re_path(r'derived_metrics$', views.derived_metrics_list),  
    re_path(r'yahoo_finance$', views.yahoo_finance),  
    re_path(r'share_price$', views.share_price),
    re_path(r'heat_map$', views.heat_map),
    re_path(r'balance_sheet$', views.balance_sheet),
    # re_path(r'metric_plot$', views.metric_plot),
    re_path(r'sentiment$', views.sentiment),
    re_path(r'risk_metric$', views.risk_metric),
    re_path(r'unique_metrics$', views.unique_metrics),
    re_path(r'read_html$', views.read_html),
    re_path(r'ownership$', views.ownership),
    re_path(r'benchmarking$', views.benchmarking),
    re_path(r'get_email$', views.get_email),
    re_path(r'get_otp$', views.get_otp)
]