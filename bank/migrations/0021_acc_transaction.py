# Generated by Django 4.2.2 on 2023-06-22 14:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0020_alter_transaction_receiver'),
    ]

    operations = [
        migrations.CreateModel(
            name='acc_transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('comment', models.CharField(default='Не указано', max_length=70)),
                ('sign', models.CharField(blank=True, choices=[('+', 'Начислить'), ('-', 'Оштрафовать')], default='+', max_length=1)),
                ('cnt', models.FloatField(default=0)),
                ('name', models.OneToOneField(help_text='Выберите кошелёк, откуда снимать (нужен Admin B.B.).', null=True, on_delete=django.db.models.deletion.SET_NULL, to='bank.account')),
            ],
        ),
    ]