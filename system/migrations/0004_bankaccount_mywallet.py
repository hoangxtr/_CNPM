# Generated by Django 3.0.7 on 2020-07-07 12:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0002_notification'),
        ('system', '0003_auto_20200706_1027'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyWallet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('my_balance', models.FloatField(default=0)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='homepage.Customer')),
            ],
        ),
        migrations.CreateModel(
            name='BankAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=128)),
                ('name', models.CharField(default='', max_length=255)),
                ('image', models.ImageField(upload_to='uploads/')),
                ('account_number', models.IntegerField(default=0)),
                ('balance', models.FloatField(default=0)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='homepage.Customer')),
            ],
        ),
    ]
