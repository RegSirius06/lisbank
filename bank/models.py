from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core import validators
import uuid

class account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.FloatField(default=0)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Уникальный ID аккаунта.")

    first_name = models.CharField(max_length=40, default='Not stated')   #   Имя
    middle_name = models.CharField(max_length=40, default='Not stated')  #   Отчество
    last_name = models.CharField(max_length=40, default='Not stated')    #   Фамилия

    EXISTING_GROUPS = (
        ('None', 'Другое'),
        ('Bi_T', 'Биология (Турчина Т.А.)'),
        ('Bi_S', 'Биология (Скороделова К.А.)'),
        ('Ch_K', 'Химия (Качалова Е.А.)'),
        ('Ch_R', 'Химия (Родионова Н.М.)'),
        ('IT_K', 'Информатика (Котова Д.А.)'),
        ('Fis1', 'Физика 1 (Шагалова А.А.)'),
        ('Fis2', 'Физика 2 (Грачёв А.А.)'),
        ('Fis3', 'Физика 3 (Дмитричева А.А.)'),
        ('Fis4', 'Физика 4 (Шевцова Т.Г.)'),
    )

    group = models.CharField(max_length=4, choices=EXISTING_GROUPS, default='None', help_text='Группа обучения')
    party = models.IntegerField(default=0)

    class Meta:
        ordering = ["party", "last_name"]
        permissions = (
            ("staff_", "Принадлежность к персоналу"),
            ("viewer", "Может смотреть какой-то отряд"),
            ("pedagogue", "Принадлежность к педагогам"),
            ("shop", "Может смотреть магазин"),
        )
    
    def get_absolute_url(self):
        return reverse('account-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name} {self.first_name[0]}.{self.middle_name[0]}.'
    
    def info(self):
        return f'{self.last_name}, {self.first_name} {self.middle_name}: {self.party} отряд, группа {self.group}'
    
    def short_name(self):
        return f'{self.last_name} {self.first_name}'
    
    def get_transactions(self):
        ret = list()
        arr = transaction.objects.all()
        for i in arr:
            if f'{i.receiver}' != f'{self}' and f'{i.creator}' != f'{self}': continue
            ret.append(i)
        return ret if ret != list() else None
    
    def renew_transactions(self):
        arr = transaction.objects.all()
        if arr is None: return 'There are no transactions'
        b = False
        for i in arr:
            if i.counted: continue
            i.count()
            b = True
        return 'Accept!' if b else 'Already accepted'

class transaction(models.Model):
    date = models.DateField(null=True)
    comment = models.CharField(max_length=70, default='Не указано')
    receiver = models.ForeignKey('account', related_name='received_trans', on_delete=models.CASCADE, null=True)
    creator = models.ForeignKey('account', related_name='created_trans', on_delete=models.CASCADE, null=True)
    counted = models.BooleanField(default=False, editable=False)

    SIGN_SET = (
        ('+', 'Начислить'),
        ('-', 'Оштрафовать'),
    )

    sign = models.CharField(max_length=1, choices=SIGN_SET, default='+')
    cnt = models.FloatField(default=0)
    
    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f'От {self.creator} к {self.receiver} на сумму {self.sign}{self.cnt}t'

    def get_sum(self):
        return f'{self.cnt}t'

    def get_absolute_url(self):
        return reverse('accounts')
    
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

    
class rule_u(models.Model):
    num_pt1 = models.IntegerField(default=1, help_text="Раздел кодекса")
    num_pt2 = models.IntegerField(default=0, help_text="Часть раздела")
    comment = models.CharField(max_length=250, default='Не указано')
    punishment = models.CharField(max_length=100, default='Не указано')
    
    def get_num(self):
        return f'УкТ {self.num_pt1}.0{self.num_pt2}' if len(f'{self.num_pt2}') == 1 else f'УкТ {self.num_pt1}.{self.num_pt2}'
    
    def __str__(self):
        return f'УкТ {self.num_pt1}.0{self.num_pt2}' if len(f'{self.num_pt2}') == 1 else f'УкТ {self.num_pt1}.{self.num_pt2}'
    
class rule_a(models.Model):
    num_pt1 = models.IntegerField(default=1, help_text="Раздел кодекса")
    num_pt2 = models.IntegerField(default=0, help_text="Часть раздела")
    comment = models.CharField(max_length=250, default='Не указано')
    punishment = models.CharField(max_length=100, default='Не указано')
    
    def get_num(self):
        return f'АкТ {self.num_pt1}.0{self.num_pt2}' if len(f'{self.num_pt2}') == 1 else f'АкТ {self.num_pt1}.{self.num_pt2}'
    
    def __str__(self):
        return f'АкТ {self.num_pt1}.0{self.num_pt2}' if len(f'{self.num_pt2}') == 1 else f'АкТ {self.num_pt1}.{self.num_pt2}'
    
class rule_t(models.Model):
    num_pt1 = models.IntegerField(default=1, help_text="Раздел кодекса")
    num_pt2 = models.IntegerField(default=0, help_text="Часть раздела")
    comment = models.CharField(max_length=250, default='Не указано')
    punishment = models.CharField(max_length=100, default='Не указано')
    
    def get_num(self):
        return f'ТкТ {self.num_pt1}.0{self.num_pt2}' if len(f'{self.num_pt2}') == 1 else f'ТкТ {self.num_pt1}.{self.num_pt2}'
    
    def __str__(self):
        return f'ТкТ {self.num_pt1}.0{self.num_pt2}' if len(f'{self.num_pt2}') == 1 else f'ТкТ {self.num_pt1}.{self.num_pt2}'
    
class rule_p(models.Model):
    num_pt1 = models.IntegerField(default=1, help_text="Раздел кодекса")
    num_pt2 = models.IntegerField(default=0, help_text="Часть раздела")
    comment = models.CharField(max_length=250, default='Не указано')
    punishment = models.CharField(max_length=100, default='Не указано')
    
    def get_num(self):
        return f'КпТ {self.num_pt1}.0{self.num_pt2}' if len(f'{self.num_pt2}') == 1 else f'КпТ {self.num_pt1}.{self.num_pt2}'
    
    def __str__(self):
        return f'КпТ {self.num_pt1}.0{self.num_pt2}' if len(f'{self.num_pt2}') == 1 else f'КпТ {self.num_pt1}.{self.num_pt2}'

class shop(models.Model):
    name = models.CharField(max_length=250, default='')
    comment = models.CharField(max_length=250, default='')
    cost = models.FloatField(default=0)
    
    def __str__(self):
        return f'{self.name} - {self.cost}t'
    
    def get_num(self):
        return f'{self.cost}t'
    
    class Meta:
        ordering = ["-cost"]
