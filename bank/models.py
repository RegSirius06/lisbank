from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
import datetime
import random
import string
import uuid
import json

class ListField(models.TextField):
    description = "Custom list field"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def from_db_value(self, value, expression, connection):
        if value is None:
            return []
        return json.loads(value)

    def to_python(self, value):
        if isinstance(value, list):
            return value
        if value is None:
            return []
        return json.loads(value)

    def get_prep_value(self, value):
        if value is None:
            return ''
        return json.dumps(value)

class account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь:")
    balance = models.FloatField(default=0, verbose_name="Баланс:")
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Уникальный ID аккаунта.")#, editable=False)

    first_name = models.CharField(max_length=40, default='Not stated', verbose_name="Имя:")        #   Имя
    middle_name = models.CharField(max_length=40, default='Not stated', verbose_name="Отчество:")  #   Отчество
    last_name = models.CharField(max_length=40, default='Not stated', verbose_name="Фамилия:")     #   Фамилия

    EXISTING_GROUPS = (
        ('None', 'Другое'),
        ('Биология 1', 'Биология 1'),
        ('Биология 2', 'Биология 2'),
        ('Химия 1', 'Химия 1'),
        ('Химия 2', 'Химия 2'),
        ('Информатика', 'Информатика'),
        ('Физика 1', 'Физика 1'),
        ('Физика 2', 'Физика 2'),
        ('Физика 3', 'Физика 3'),
        ('Физика 4', 'Физика 4'),
    )

    user_group = models.CharField(max_length=40, choices=EXISTING_GROUPS, default='None', help_text='Группа обучения', verbose_name="Занятия:")
    party = models.IntegerField(default=0, verbose_name="Отряд:")
    account_status = models.CharField(max_length=100, default='', blank=True, verbose_name="Статус:")

    class Meta:
        ordering = ["party", "last_name"]
        permissions = (
            ("staff_", "Принадлежность к персоналу"),
            ("transaction", "Может создавать транзакции"),
            ("transaction_base", "Может совершать переводы"),
            ("register", "Может регистрировать пользователей"),
            ("edit_users", "Может изменять пользователей"),
            ("meria", "Мэрия в банке"),
        )
    
    def get_absolute_url(self):
        return reverse('account-detail', args=[str(self.id)])
    
    def get_absolute_url_for_edit(self):
        return reverse('account-edit-n', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name} {self.first_name[0]}.{self.middle_name[0]}.'
    
    def info(self):
        return f'{self.last_name}, {self.first_name} {self.middle_name}: {self.party} отряд, группа {self.user_group}'
    
    def short_name(self):
        return f'{self.last_name} {self.first_name}'
    
    def get_status(self):
        return f'"{self.account_status}"' if self.account_status != '' else 'не установлен'
    
    def is_ped(self):
        group = self.user.groups.get(name="pedagogue")
        return group is not None

    def get_transactions(self):
        ret = list()
        arr = transaction.objects.all()
        for i in arr:
            if f'{i.receiver}' != f'{self}' and f'{i.creator}' != f'{self}':
                if f'{self.party}' != f'{i.receiver.last_name[-1]}': continue
            ret.append(i)
        return ret if ret != list() else None

    def account_valid(self, x):
        return f'{self.party}'

    def renew_transactions(self):
        arr = transaction.objects.all()
        if arr is None: return 'There are no transactions'
        b = False
        for i in arr:
            if i.counted: continue
            i.count()
            b = True
        return 'Accept!' if b else 'Already accepted'
    
    def undo_transactions(self):
        arr = transaction.objects.all()
        if arr is None: return 'There are no transactions'
        b = False
        for i in arr:
            if not i.counted: continue
            i.uncount()
            b = True
        return 'Accept!' if b else 'Already accepted'
    
    def update_passwords(self):
        def check_user_in_group(user, group_name): return user.groups.filter(name=group_name).exists()
        def gen_pass(length: int) -> str:
            lang = []
            hard_to_read = "l1IioO0"
            for i in string.printable[:62]:
                if i in hard_to_read: continue
                lang.append(i)
            list_ = []
            for u in User.objects.all():
                list_.append(u.password)
            set_list = set(list_)
            while True:
                pas = ""
                for i in range(length):
                    el = random.choice(lang)
                    pas += el
                if pas not in set_list:
                    return pas
        users = User.objects.all().exclude(username__icontains='admin')
        s_write = '-' * 30 + '\n'
        for u in users:
            len_pass = 12 if check_user_in_group(u, 'pedaogue') else 8
            username = u.username
            password = gen_pass(len_pass)
            s_write += f'login: {username}\npassword: {password}\n' + '-' * 30 + '\n'
            u.set_password(make_password(password))
        f = open("All_users.txt", "w")
        f.write(s_write)
        f.close()
        return "Done!"

class transaction(models.Model):
    date = models.DateField(null=True)
    comment = models.CharField(max_length=70, default='Не указано')
    receiver = models.ForeignKey('account', related_name='received_trans', on_delete=models.CASCADE, null=True, verbose_name="Получатель:")
    creator = models.ForeignKey('account', related_name='created_trans', on_delete=models.CASCADE, null=True, verbose_name="Отправитель:")
    history = models.ForeignKey('account', related_name='history_trans', on_delete=models.CASCADE, null=True, verbose_name="Создатель:")
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Уникальный ID транзакции.")
    counted = models.BooleanField(default=False, editable=False)

    SIGN_SET = (
        ('+', 'Начислить'),
        ('-', 'Оштрафовать'),
    )

    sign = models.CharField(max_length=1, choices=SIGN_SET, default='+', verbose_name="Тип транзакции:")
    cnt = models.FloatField(default=0, verbose_name="Количество:")
    
    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f'От {self.creator} к {self.receiver} на сумму {self.sign}{self.cnt}t (Создал {self.history}): {self.comment}'

    def get_sum(self):
        return f'{self.cnt}t'

    def transaction_valid(self, x):
        return f'{self.receiver.last_name[-1]}'

    def get_absolute_url(self):
        return reverse('transaction-detail', args=[str(self.id)])

    def get_absolute_url_for_edit(self):
        return reverse('transaction-edit', args=[str(self.id)])
    
    def count(self):
        if self.counted: return
        rec = self.receiver
        crt = self.creator
        if self.sign == '+':
            rec.balance = rec.balance + self.cnt
            rec.save()
            crt.balance = crt.balance - self.cnt
            crt.save()
        else:
            rec.balance = rec.balance - self.cnt
            rec.save()
            crt.balance = crt.balance + self.cnt
            crt.save()
        self.counted = True
        self.save()
        return
    
    def uncount(self):
        if not self.counted: return
        rec = self.receiver
        crt = self.creator
        if self.sign == '+':
            rec.balance = rec.balance - self.cnt
            rec.save()
            crt.balance = crt.balance + self.cnt
            crt.save()
        else:
            rec.balance = rec.balance + self.cnt
            rec.save()
            crt.balance = crt.balance - self.cnt
            crt.save()
        self.counted = False
        self.save()
        return

class rools(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Уникальный ID.")
    
    EXISTING_TYPES_OF_RULES = (
        ('УкТ', 'Уголовный кодекс'),
        ('АкТ', 'Административный кодекс'),
        ('ТкТ', 'Трудовой кодекс'),
        ('КпТ', 'Кодекс премий'),
    )

    num_type = models.CharField(max_length=3, choices=EXISTING_TYPES_OF_RULES, default='УкТ', verbose_name="Раздел законов:")
    
    num_pt1 = models.IntegerField(default=1, help_text="Раздел кодекса")
    num_pt2 = models.IntegerField(default=0, help_text="Часть раздела")
    comment = models.CharField(max_length=250, default='Не указано')
    punishment = models.CharField(max_length=100, default='Не указано')
    
    class Meta:
        ordering = ["num_type", "num_pt1", "num_pt2"]

    def get_num(self):
        return f'{self.num_type} {self.num_pt1}.0{self.num_pt2}' if len(f'{self.num_pt2}') == 1 else f'УкТ {self.num_pt1}.{self.num_pt2}'
    
    def __str__(self):
        return f'УкТ {self.num_pt1}.0{self.num_pt2}' if len(f'{self.num_pt2}') == 1 else f'УкТ {self.num_pt1}.{self.num_pt2}'

class shop(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Уникальный ID.")
    name = models.CharField(max_length=250, default='', verbose_name="Название:")
    comment = models.CharField(max_length=250, default='', verbose_name="Комментарий:")
    cost = models.FloatField(default=0, verbose_name="Цена:")
    
    def __str__(self):
        return f'{self.name} - {self.cost}t'
    
    def get_num(self):
        return f'{self.cost}t'
    
    def get_absolute_url(self):
        return reverse('shop-renew', args=[str(self.id)])
    
    class Meta:
        ordering = ["-cost"]

class plan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Уникальный ID.")
    time = models.CharField(max_length=250, default='', verbose_name="Во сколько:")
    comment = models.CharField(max_length=250, default='', verbose_name="Комментарий:")
    number = models.IntegerField(default=0, verbose_name="Номер в списке: ")
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Уникальный ID.")
    
    def __str__(self):
        return f'{self.number} - {self.time}; {self.comment}'
    
    def get_absolute_url(self):
        return reverse('plans-renew', args=[str(self.id)])
    
    class Meta:
        ordering = ["number"]

class message(models.Model):
    date = models.DateField(verbose_name="Дата:")
    time = models.TimeField(default=datetime.time(hour=0), verbose_name="Время:")
    receiver = models.ForeignKey('chat', related_name='received_mess', blank=True, on_delete=models.CASCADE, null=True, verbose_name="Получатель:")
    creator = models.ForeignKey('account', related_name='created_mess', on_delete=models.CASCADE, null=True, verbose_name="Отправитель:")
    text = models.TextField(max_length=2000, verbose_name='Текст:')
    anonim = models.BooleanField(default=False, verbose_name='Если вы хотите отправить это сообщение анонимно, поставьте здесь галочку.')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Уникальный ID сообщения.")
    anonim_legacy = models.BooleanField(default=False, editable=False)

    def get_absolute_url(self):
        x = chat_valid.objects.get(what_chat=self.receiver) if self.receiver is not None else None
        flag = x is not None
        if not flag: 
            flag = self.receiver is None
            print('nok')
        else: flag = x.avaliable
        return reverse('messages-edit-n', args=[str(self.id)]) if flag else None
    
    def get_date(self):
        return f'{self.date} в {self.time}'.split('.')[0]
    
    def anonim_status(self):
        return 'Анонимно' if self.anonim or self.anonim_legacy else 'Публично'

    def __str__(self):
        return f'{self.date}: ' + ('(глобально)' if self.receiver is None else f'К {self.receiver}') + (f' от {self.creator}' if not self.anonim else ' (анонимно)')
    
    class Meta:
        ordering = ["-date", "-time"]

class chat(models.Model):
    cnt = models.IntegerField(default=1, editable=False)
    name = models.CharField(max_length=50, default='', verbose_name='Название чата:')
    description = models.CharField(max_length=500, default='', verbose_name='Описание чата:')
    creator = models.ForeignKey('account', related_name='creator_chat', on_delete=models.CASCADE, null=True, verbose_name="Создатель:")
    anonim = models.BooleanField(default=False, verbose_name='Если вы хотите сделать чат анонимным, поставьте здесь галочку. Этот параметр неизменяем.')
    anonim_legacy = models.BooleanField(default=False, verbose_name='Поставьте галочку, если хотите разрешить участникам отправлять анонимные сообщения.')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Уникальный ID чата.")

    def __str__(self):
        return f'{self.name} (создал {self.creator}): {self.cnt} участников'

    def get_absolute_url(self):
        return reverse('chats-n', args=[str(self.id)]) if chat_valid.objects.get(what_chat=self).avaliable else None

    def get_absolute_url_for_edit(self):
        return reverse('chats-edit-n', args=[str(self.id)]) if chat_valid.objects.get(what_chat=self).avaliable else None

    def get_absolute_url_from_archive(self):
        return reverse('chats-archived-n', args=[str(self.id)])
    
    def anonim_status(self):
        return 'Анонимный чат' if self.anonim else \
               'Анонимные сообщения разрешены' if self.anonim_legacy\
                else 'Все сообщения публичные'

    def archive(self):
        chat_validator = chat_valid.objects.get(what_chat=self)
        chat_validator.avaliable = False
        list_x = chat_validator.get_all_CAA()
        for i in list_x: i.read_chat()
        chat_validator.save()

    def get_read_status(self, acc: account):
        CAA = chat_and_acc.objects.filter(what_chat=self).get(what_acc=acc)
        return CAA.readen

    def chat_valid(self):
        return f'{self}'

    class Meta:
        ordering = ["name"]

class chat_valid(models.Model):
    what_chat = models.OneToOneField('chat', on_delete=models.CASCADE, null=True, verbose_name="Чат:")
    avaliable = models.BooleanField(default=True, editable=False)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Уникальный ID.")
    list_members = ListField(default=[], null=True, help_text="Список ID участников:")
    list_messages = ListField(default=[], null=True, help_text="Список ID сообщений:")

    def __str__(self):
        return f'{self.what_chat} ' + ('(доступен)' if self.avaliable else '(не доступен)')
    
    def getting_access(self, acc: account):
        for i in self.list_members:
            if f'{acc.id}' == f'{i}': return True
        return False
    
    def getting_access_id(self, acc: uuid):
        for i in self.list_members:
            if f'{acc}' == f'{i}': return True
        return False
    
    def add_msg(self, msg: message):
        if self.list_messages is None:
            self.list_messages = []
        self.list_messages.append(f'{msg.id}')
        list_x = list(self.get_all_CAA())
        for i in list_x:
            i.readen = False
            i.save()
        self.save()
        return
    
    def get_all_msg(self):
        list_x = [uuid.UUID(i) for i in self.list_messages]
        return message.objects.filter(id__in=list_x)
    
    def get_all_CAA(self):
        return chat_and_acc.objects.filter(what_chat=self.what_chat)

class chat_and_acc(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Уникальный ID.")
    what_chat = models.ForeignKey('chat', on_delete=models.CASCADE, null=True, verbose_name="Чат:")
    what_acc = models.ForeignKey('account', on_delete=models.CASCADE, null=True, verbose_name="Аккаунт:")
    readen = models.BooleanField(default=False, editable=False)

    def __str__(self):
        return f'{self.what_chat} ' + ('(' if self.readen else '(не ') + f'прочитан {self.what_acc})'

    def valid_CAA(self):
        return f'{self.what_chat}'

    def read_chat(self):
        self.readen = True
        self.save()
        return
    
    def unread_chat(self):
        self.readen = False
        self.save()
        return

class daily_answer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Уникальный ID.")
    name = models.TextField(max_length=500, verbose_name='Название задачи:', default='none')
    text = models.TextField(max_length=1000, verbose_name='Условие задачи:')
    cnt = models.FloatField(default=0, verbose_name="Награда:")
    status = models.BooleanField(default=False, verbose_name="Это задача смены?")

    class Meta:
        ordering = ["cnt"]

    def __str__(self):
        return f'{self.name}: на {self.cnt}'
    
    def get_absolute_url(self):
        return reverse('answers-renew', args=[str(self.id)])
