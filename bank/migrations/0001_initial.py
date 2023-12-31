# Generated by Django 4.2.2 on 2023-07-24 12:47

import bank.models
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='account',
            fields=[
                ('balance', models.FloatField(default=0, verbose_name='Баланс:')),
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Уникальный ID аккаунта.', primary_key=True, serialize=False)),
                ('first_name', models.CharField(default='Not stated', max_length=40, verbose_name='Имя:')),
                ('middle_name', models.CharField(default='Not stated', max_length=40, verbose_name='Отчество:')),
                ('last_name', models.CharField(default='Not stated', max_length=40, verbose_name='Фамилия:')),
                ('user_group', models.CharField(choices=[('None', 'Другое'), ('Биология 1', 'Биология 1'), ('Биология 2', 'Биология 2'), ('Химия 1', 'Химия 1'), ('Химия 2', 'Химия 2'), ('Информатика', 'Информатика'), ('Физика 1', 'Физика 1'), ('Физика 2', 'Физика 2'), ('Физика 3', 'Физика 3'), ('Физика 4', 'Физика 4')], default='None', help_text='Группа обучения', max_length=40, verbose_name='Занятия:')),
                ('party', models.IntegerField(default=0, verbose_name='Отряд:')),
                ('account_status', models.CharField(blank=True, default='', max_length=100, verbose_name='Статус:')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь:')),
            ],
            options={
                'ordering': ['party', 'last_name'],
                'permissions': (('staff_', 'Принадлежность к персоналу'), ('transaction', 'Может создавать транзакции'), ('transaction_base', 'Может совершать переводы'), ('register', 'Может регистрировать пользователей'), ('edit_users', 'Может изменять пользователей'), ('meria', 'Мэрия в банке')),
            },
        ),
        migrations.CreateModel(
            name='chat',
            fields=[
                ('cnt', models.IntegerField(default=1, editable=False)),
                ('name', models.CharField(default='', max_length=50, verbose_name='Название чата:')),
                ('description', models.CharField(default='', max_length=500, verbose_name='Описание чата:')),
                ('anonim', models.BooleanField(default=False, verbose_name='Если вы хотите сделать чат анонимным, поставьте здесь галочку. Этот параметр неизменяем.')),
                ('anonim_legacy', models.BooleanField(default=False, verbose_name='Поставьте галочку, если хотите разрешить участникам отправлять анонимные сообщения.')),
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Уникальный ID чата.', primary_key=True, serialize=False)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='creator_chat', to='bank.account', verbose_name='Создатель:')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='daily_answer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Уникальный ID.', primary_key=True, serialize=False)),
                ('name', models.TextField(default='none', max_length=500, verbose_name='Название задачи:')),
                ('text', models.TextField(max_length=1000, verbose_name='Условие задачи:')),
                ('cnt', models.FloatField(default=0, verbose_name='Награда:')),
                ('status', models.BooleanField(default=False, verbose_name='Это задача смены?')),
            ],
            options={
                'ordering': ['cnt'],
            },
        ),
        migrations.CreateModel(
            name='plan',
            fields=[
                ('time', models.CharField(default='', max_length=250, verbose_name='Во сколько:')),
                ('comment', models.CharField(default='', max_length=250, verbose_name='Комментарий:')),
                ('number', models.IntegerField(default=0, verbose_name='Номер в списке: ')),
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Уникальный ID.', primary_key=True, serialize=False)),
            ],
            options={
                'ordering': ['number'],
            },
        ),
        migrations.CreateModel(
            name='rools',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Уникальный ID.', primary_key=True, serialize=False)),
                ('num_type', models.CharField(choices=[('УкТ', 'Уголовный кодекс'), ('АкТ', 'Административный кодекс'), ('ТкТ', 'Трудовой кодекс'), ('КпТ', 'Кодекс премий')], default='УкТ', max_length=3, verbose_name='Раздел законов:')),
                ('num_pt1', models.IntegerField(default=1, help_text='Раздел кодекса')),
                ('num_pt2', models.IntegerField(default=0, help_text='Часть раздела')),
                ('comment', models.CharField(default='Не указано', max_length=250)),
                ('punishment', models.CharField(default='Не указано', max_length=100)),
            ],
            options={
                'ordering': ['num_type', 'num_pt1', 'num_pt2'],
            },
        ),
        migrations.CreateModel(
            name='shop',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Уникальный ID.', primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=250, verbose_name='Название:')),
                ('comment', models.CharField(default='', max_length=250, verbose_name='Комментарий:')),
                ('cost', models.FloatField(default=0, verbose_name='Цена:')),
            ],
            options={
                'ordering': ['-cost'],
            },
        ),
        migrations.CreateModel(
            name='transaction',
            fields=[
                ('date', models.DateField(null=True)),
                ('comment', models.CharField(default='Не указано', max_length=70)),
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Уникальный ID транзакции.', primary_key=True, serialize=False)),
                ('counted', models.BooleanField(default=False, editable=False)),
                ('sign', models.CharField(choices=[('+', 'Начислить'), ('-', 'Оштрафовать')], default='+', max_length=1, verbose_name='Тип транзакции:')),
                ('cnt', models.FloatField(default=0, verbose_name='Количество:')),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_trans', to='bank.account', verbose_name='Отправитель:')),
                ('history', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='history_trans', to='bank.account', verbose_name='Создатель:')),
                ('receiver', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='received_trans', to='bank.account', verbose_name='Получатель:')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='message',
            fields=[
                ('date', models.DateField(verbose_name='Дата:')),
                ('time', models.TimeField(default=datetime.time(0, 0), verbose_name='Время:')),
                ('text', models.TextField(max_length=2000, verbose_name='Текст:')),
                ('anonim', models.BooleanField(default=False, verbose_name='Если вы хотите отправить это сообщение анонимно, поставьте здесь галочку.')),
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Уникальный ID сообщения.', primary_key=True, serialize=False)),
                ('anonim_legacy', models.BooleanField(default=False, editable=False)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_mess', to='bank.account', verbose_name='Отправитель:')),
                ('receiver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='received_mess', to='bank.chat', verbose_name='Получатель:')),
            ],
            options={
                'ordering': ['-date', '-time'],
            },
        ),
        migrations.CreateModel(
            name='chat_valid',
            fields=[
                ('avaliable', models.BooleanField(default=True, editable=False)),
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Уникальный ID.', primary_key=True, serialize=False)),
                ('list_members', bank.models.ListField(default=[], help_text='Список ID участников:', null=True)),
                ('list_messages', bank.models.ListField(default=[], help_text='Список ID сообщений:', null=True)),
                ('what_chat', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='bank.chat', verbose_name='Чат:')),
            ],
        ),
        migrations.CreateModel(
            name='chat_and_acc',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Уникальный ID.', primary_key=True, serialize=False)),
                ('readen', models.BooleanField(default=False, editable=False)),
                ('what_acc', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bank.account', verbose_name='Аккаунт:')),
                ('what_chat', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bank.chat', verbose_name='Чат:')),
            ],
        ),
    ]
