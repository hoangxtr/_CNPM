# Generated by Django 3.0.8 on 2020-07-09 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0006_auto_20200708_2345'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='complete',
        ),
        migrations.RemoveField(
            model_name='order',
            name='is_shipping',
        ),
        migrations.RemoveField(
            model_name='order',
            name='to_chef',
        ),
        migrations.AddField(
            model_name='order',
            name='step',
            field=models.IntegerField(default=0),
        ),
    ]
