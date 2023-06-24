# Generated by Django 4.2.2 on 2023-06-21 08:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0013_remove_money_sign_transaction_sign'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='whose_account',
        ),
        migrations.AddField(
            model_name='transaction',
            name='name',
            field=models.OneToOneField(help_text='Выберите кошелёк.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='bank.money'),
        ),
    ]
