# Generated by Django 2.1.7 on 2019-05-12 18:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('miniproject', '0006_auto_20190512_1032'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='Question',
        ),
        migrations.DeleteModel(
            name='Document',
        ),
    ]
