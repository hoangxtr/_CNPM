# Generated by Django 3.0.7 on 2020-07-08 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0004_bankaccount_mywallet'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bankaccount',
            name='user',
        ),
        migrations.AddField(
            model_name='mywallet',
            name='my_account_number',
            field=models.IntegerField(default=0),
        ),
    ]
