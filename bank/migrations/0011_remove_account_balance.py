# Generated by Django 4.2.2 on 2023-06-21 08:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0010_money_alter_account_options_remove_transaction_sign'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='balance',
        ),
    ]
