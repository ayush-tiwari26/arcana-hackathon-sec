from rest_framework import serializers
from dashboard_api.models import Companies, DerivedMetrics, BaseMetrics, RiskModel, SentimentModel


class CompaniesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Companies
        fields = ('cik',
            'name',
            'ticker',
            'website',
            'addresses',
            'phone',
            'sic',
            'category',
            'overview',
            'founding_year',
            'state_of_incorporation'
        )

class ShortCompaniesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Companies
        fields = ('cik',
            'name',
        )

class DerivedMetricsSerializer(serializers.ModelSerializer):
    company = ShortCompaniesSerializer()

    class Meta:
        model = DerivedMetrics
        fields = (
            'company',
            'tag',
            'value',
            'formula',
            'description',
            'filing_date',
            'sentence_date',
            'accession_no',
            'form_type',  
            'description',
            'source',
            'sentence',
            'score'
        )
     

class BaseMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseMetrics
        fields = (
            'tag',
            'company',
            'value',
            'decimel',
            'unit',
            'form_type',
            'accession_no',
            'filing_date',
            'source'
        )

class RiskModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiskModel
        fields = (
            'company',
            'filing_date',
            'financial',
            'otheridiosyncracies',
            'legal',
            'othersystematic',
            'tax'
        )

class SentimentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SentimentModel
        fields = (
            'company',
            'filing_date',
            'confidence',
            'label',
            'positive',
            'negative',
            'type',
            'item'
        )