# Generated by Django 4.2.2 on 2023-06-20 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0004_alter_transaction_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rool',
            name='group',
        ),
        migrations.AddField(
            model_name='rool',
            name='num_pt1',
            field=models.CharField(blank=True, choices=[('УкТ', 'Уголовный кодекс'), ('АкТ', 'Административный кодекс'), ('ТкТ', 'Трудовой кодекс'), ('КпТ', 'Кодекс премий'), ('N', 'None')], default='N', help_text='Тип закона', max_length=3),
        ),
    ]