# Generated by Django 4.2.2 on 2023-06-23 16:04

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0033_transaction_remove_transaction_staff_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='recipient',
        ),
        migrations.AddField(
            model_name='transaction',
            name='receiver',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='received_trans', to='bank.account'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='cnt',
            field=models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(0.0)]),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_trans', to='bank.account'),
        ),
    ]