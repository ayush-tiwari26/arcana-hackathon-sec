# Generated by Django 4.0.3 on 2022-03-11 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard_api', '0002_alter_basemetrics_unit'),
    ]

    operations = [
        migrations.AddField(
            model_name='basemetrics',
            name='source',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
