# Generated by Django 2.2.3 on 2019-10-18 03:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deal', '0009_auto_20191017_1803'),
    ]

    operations = [
        migrations.AddField(
            model_name='lastdayassets',
            name='currency_status',
            field=models.CharField(default='0', max_length=10),
        ),
    ]
