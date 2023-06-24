# Generated by Django 4.2.2 on 2023-06-23 09:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0030_remove_transaction_name_remove_transaction_receiver_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='transaction_base',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('comment', models.CharField(default='Не указано', max_length=70)),
                ('cnt', models.FloatField(default=0)),
                ('name', models.ForeignKey(help_text='Выберите, кому вы хотите перевести средства.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='bank.account')),
            ],
        ),
        migrations.CreateModel(
            name='transaction_staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('comment', models.CharField(default='Не указано', max_length=70)),
                ('sign', models.CharField(blank=True, choices=[('+', 'Начислить'), ('-', 'Оштрафовать')], default='+', max_length=1)),
                ('cnt', models.FloatField(default=0)),
                ('name', models.ForeignKey(help_text='Выберите кошелёк, который премируется/штрафуется.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='bank.account')),
            ],
        ),
        migrations.DeleteModel(
            name='transaction',
        ),
    ]
