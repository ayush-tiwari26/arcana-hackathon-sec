# Generated by Django 3.2 on 2022-03-17 10:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard_api', '0007_auto_20220317_1055'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='basemetrics',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='basemetrics',
            name='start_date',
        ),
        migrations.RemoveField(
            model_name='derivedmetrics',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='derivedmetrics',
            name='start_date',
        ),
    ]