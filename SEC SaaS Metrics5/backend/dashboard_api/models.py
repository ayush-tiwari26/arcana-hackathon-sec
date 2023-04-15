from email.policy import default
from hashlib import blake2s
from random import choices
from statistics import mode
from wsgiref.simple_server import demo_app
from django.db import models
from datetime import datetime


SOURCE_CHOICES = [
    ('10-K', '10-K Filing'),
    ('10-Q', '10-Q Filing'),
    ('8-K', '8-K Filing'),
    ('YF', 'Yahoo Finance'),
    ('BB', 'Bloomberg'),
    ('OT', 'Other'),
]

class Companies(models.Model):
    cik = models.CharField(max_length=15, blank=True)
    name = models.CharField(max_length=50)
    ticker = models.CharField(max_length=200,blank=True,null=True)
    website = models.CharField(max_length=200,blank=True,null=True)
    addresses = models.CharField(max_length=500,blank=True,null=True)
    phone = models.CharField(max_length=20,blank=True,null=True)
    overview = models.CharField(max_length=1000, blank=True, null=True)
    sic = models.CharField(max_length = 6,blank = True,null=True)
    category = models.CharField(max_length = 150,blank  = True,null=True)
    state_of_incorporation = models.CharField(max_length = 150,blank = True,null=True)
    founding_year = models.CharField(max_length=5, blank=True, null=True)

    def __str__(self):
        return self.name

class BaseMetrics(models.Model):
    company = models.ForeignKey(Companies, on_delete=models.CASCADE, null=True, default="")
    tag = models.CharField(max_length = 300)
    value = models.FloatField(max_length=100, blank=True)
    decimel = models.CharField(max_length=100, blank=True)
    unit = models.CharField(max_length=100, blank=True)
    accession_no = models.CharField(max_length=50, blank=True)
    filing_date = models.DateField(null=True,blank=True)
    form_type = models.CharField(max_length=20, choices=SOURCE_CHOICES, default="OT")
    source = models.CharField(max_length=10, blank=True)



    def __str__(self):
        return self.company.name + "_"+ self.tag

class DerivedMetrics(models.Model):

    company = models.ForeignKey(Companies, on_delete=models.CASCADE, null=True, default="")
    value = models.FloatField(max_length=100, blank=True)
    formula = models.CharField(max_length=300, blank=True)
    form_type = models.CharField(max_length=20, choices=SOURCE_CHOICES, default="OT")
    filing_date = models.DateField(blank=True, null=True)
    accession_no = models.CharField(max_length=50, blank=True)
    unit = models.CharField(max_length=10, blank=True)
    tag = models.CharField(max_length = 300)    
    base_metrics = models.ManyToManyField(BaseMetrics)
    description = models.CharField(max_length=1000, blank=True)
    sentence = models.CharField(max_length=5000, blank=True)
    sentence_date = models.CharField(max_length=100, blank=True)
    score = models.FloatField(max_length=100, blank=True, default=0)
    source = models.CharField(max_length=10, blank=True, default="xbrl")


    def __str__(self):
        return self.company.name + "__" + self.tag

class RiskModel(models.Model):

    company = models.ForeignKey(Companies, on_delete=models.CASCADE, null=True, default="")
    filing_date = models.CharField(max_length=100, blank=True,null=True)
    financial = models.FloatField(max_length=100, blank=True)
    otheridiosyncracies = models.FloatField(max_length=100, blank=True)
    legal = models.FloatField(max_length=100, blank=True)
    othersystematic = models.FloatField(max_length=100, blank=True)
    tax = models.FloatField(max_length=100, blank=True)

    def __str__(self):
        return self.company.name 

class SentimentModel(models.Model):

    company = models.ForeignKey(Companies, on_delete=models.CASCADE, null=True, default="")
    filing_date = models.DateField(max_length=100, blank=True,null=True)
    confidence = models.FloatField(max_length=100, blank=True)
    label = models.CharField(max_length=100, blank=True)
    positive = models.CharField(max_length=1000, blank=True)
    negative = models.CharField(max_length=1000, blank=True)
    type = models.CharField(max_length=100, blank=True)
    item = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.company.name+ "__" + str(self.filing_date )
