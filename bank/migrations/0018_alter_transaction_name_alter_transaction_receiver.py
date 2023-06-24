# Generated by Django 4.2.2 on 2023-06-21 11:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0017_transaction_receiver_alter_money_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='name',
            field=models.OneToOneField(help_text='Выберите кошелёк, откуда снимать (нужен Admin B.B.).', null=True, on_delete=django.db.models.deletion.SET_NULL, to='bank.money'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='receiver',
            field=models.OneToOneField(help_text='Чей кошелёк оштрафован/премирован?', null=True, on_delete=django.db.models.deletion.SET_NULL, to='bank.account'),
        ),
    ]
