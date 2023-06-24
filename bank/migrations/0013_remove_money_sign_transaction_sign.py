# Generated by Django 4.2.2 on 2023-06-21 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0012_alter_money_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='money',
            name='sign',
        ),
        migrations.AddField(
            model_name='transaction',
            name='sign',
            field=models.CharField(blank=True, choices=[('N', 'None'), ('+', 'Начислить'), ('-', 'Оштрафовать')], default='N', help_text='Если None, то непосредственно счёт пионера.', max_length=1),
        ),
    ]