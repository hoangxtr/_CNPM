# Generated by Django 2.0.13 on 2020-07-08 13:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0004_auto_20200708_2040'),
        ('homepage', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='admin',
            name='user',
        ),
        migrations.RemoveField(
            model_name='chef',
            name='user',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='user',
        ),
        migrations.DeleteModel(
            name='Admin',
        ),
        migrations.DeleteModel(
            name='Chef',
        ),
        migrations.DeleteModel(
            name='Customer',
        ),
    ]