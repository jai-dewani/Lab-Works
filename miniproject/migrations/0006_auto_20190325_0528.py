# Generated by Django 2.1.7 on 2019-03-25 05:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miniproject', '0005_auto_20190325_0448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='created',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 3, 25, 5, 28, 49, 323729)),
        ),
    ]