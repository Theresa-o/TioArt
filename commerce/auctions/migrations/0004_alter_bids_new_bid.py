# Generated by Django 4.0.2 on 2022-03-10 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_alter_bids_auction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bids',
            name='new_bid',
            field=models.IntegerField(),
        ),
    ]
