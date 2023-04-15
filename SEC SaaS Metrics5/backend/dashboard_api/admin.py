from django.contrib import admin

from .models import Companies, DerivedMetrics, BaseMetrics,RiskModel,SentimentModel

admin.site.register(Companies)
admin.site.register(DerivedMetrics)
admin.site.register(BaseMetrics)
admin.site.register(RiskModel)
admin.site.register(SentimentModel)

