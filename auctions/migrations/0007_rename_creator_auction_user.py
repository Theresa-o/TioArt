# Generated by Django 4.0.2 on 2022-03-17 07:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_rename_user_auction_creator'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auction',
            old_name='creator',
            new_name='user',
        ),
    ]