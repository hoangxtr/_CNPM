# Generated by Django 3.0.7 on 2020-07-11 01:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='store',
        ),
    ]
