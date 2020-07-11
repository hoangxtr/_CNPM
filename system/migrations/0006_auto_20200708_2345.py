# Generated by Django 2.0.13 on 2020-07-08 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0005_order_received'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='received',
            new_name='is_shipping',
        ),
        migrations.AddField(
            model_name='order',
            name='to_chef',
            field=models.BooleanField(default=False),
        ),
    ]