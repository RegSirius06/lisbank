# Generated by Django 4.2.2 on 2023-06-21 11:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0016_alter_transaction_non_exit'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='receiver',
            field=models.OneToOneField(help_text='Куда', null=True, on_delete=django.db.models.deletion.SET_NULL, to='bank.account'),
        ),
        migrations.AlterField(
            model_name='money',
            name='name',
            field=models.OneToOneField(help_text='Чей кошелёк?', null=True, on_delete=django.db.models.deletion.SET_NULL, to='bank.account'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='sign',
            field=models.CharField(blank=True, choices=[('+', 'Начислить'), ('-', 'Оштрафовать')], default='+', help_text='Если None, то непосредственно счёт пионера.', max_length=1),
        ),
    ]
