# Generated by Django 4.0.2 on 2022-03-17 07:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_rename_current_bid_auction_starting_bid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auction',
            old_name='user',
            new_name='creator',
        ),
    ]