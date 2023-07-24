from typing import Any, Dict
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from bank.models import account, transaction, message, rools, plan, daily_answer, shop, chat, chat_and_acc, chat_valid
from django.core.paginator import Paginator
import datetime
import uuid

class SetStatus(forms.Form):
    status = forms.CharField(max_length=50, required=False, label="Введите новый статус:")

    def clean_status(self):
        return self.cleaned_data['status']

class SetReadStatusForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class NewTransactionStaffForm(forms.Form):
    transaction_date = forms.DateField(help_text="Дата должна быть в пределах смены, по умолчанию сегодня.", label="Дата:")

    def clean_transaction_date(self):
        data = self.cleaned_data['transaction_date']
        if data < datetime.date(year=2024, month=6, day=25):
            raise ValidationError(_('Вы указали дату до смены.'))
        if data > datetime.date(year=2024, month=6, day=25) + datetime.timedelta(weeks=3):
            raise ValidationError(_('Вы указали дату после смены.'))
        return data
    
    list_accounts = account.objects.exclude(party=0)
    transaction_receiver = forms.ModelChoiceField(queryset=list_accounts, label="Получатель:")#, widget=forms.RadioSelect()) 
    
    def clean_transaction_receiver(self):
            return self.cleaned_data['transaction_receiver']

    transaction_cnt = forms.FloatField(help_text="Укажите сумму перевода.", label="Сумма:")

    def clean_transaction_cnt(self):
        cnt = self.cleaned_data['transaction_cnt']
        if cnt <= 0:
            raise ValidationError(_('Вы не можете ввести сумму средств меньше нуля или ноль.'))
        return cnt

    transaction_comment = forms.CharField(help_text="Пояснение начисления/штрафа.", label="Комментарий:")

    def clean_transaction_comment(self):
        return self.cleaned_data['transaction_comment']
    
    transaction_sign = forms.ChoiceField(choices=transaction.SIGN_SET, help_text="Выберите тип: премия/штраф", label="Тип транзакции:")
    
    def clean_transaction_sign(self):
            return self.cleaned_data['transaction_sign']
    
    class Meta:
        model = transaction
        fields = ['transaction_date', 'transaction_receiver', 'transaction_cnt', 'transaction_comment', 'transaction_sign']

class NewTransactionStaffFormParty(forms.Form):
    transaction_date = forms.DateField(help_text="Дата должна быть в пределах смены, по умолчанию сегодня.", label="Дата:")

    def clean_transaction_date(self):
        data = self.cleaned_data['transaction_date']
        if data < datetime.date(year=2024, month=6, day=25):
            raise ValidationError(_('Вы указали дату до смены.'))
        if data > datetime.date(year=2024, month=6, day=25) + datetime.timedelta(weeks=3):
            raise ValidationError(_('Вы указали дату после смены.'))
        return data
    
    transaction_receiver = forms.IntegerField(label="Получатель:", help_text="Введите номер отряда.")
    
    def clean_transaction_receiver(self):
            list_accounts = set([i.party for i in account.objects.all() if i.party != 0])
            x = int(self.cleaned_data['transaction_receiver'])
            if x <= 0:
                raise ValidationError(_('Вы не можете выбрать служебные отряды.'))
            if x not in list_accounts:
                raise ValidationError(_('Такого отряда не существует.'))
            return x

    transaction_cnt = forms.FloatField(help_text="Укажите сумму перевода.", label="Сумма:")

    def clean_transaction_cnt(self):
        cnt = self.cleaned_data['transaction_cnt']
        if cnt <= 0:
            raise ValidationError(_('Вы не можете ввести сумму средств меньше нуля или ноль.'))
        return cnt

    transaction_comment = forms.CharField(help_text="Пояснение начисления/штрафа.", label="Комментарий:")

    def clean_transaction_comment(self):
        return self.cleaned_data['transaction_comment']
    
    transaction_sign = forms.ChoiceField(choices=transaction.SIGN_SET, help_text="Выберите тип: премия/штраф", label="Тип транзакции:")
    
    def clean_transaction_sign(self):
            return self.cleaned_data['transaction_sign']

class NewTransactionFullForm(forms.Form):
    transaction_date = forms.DateField(help_text="Дата должна быть в пределах смены, по умолчанию сегодня.", label="Дата:")

    def clean_transaction_date(self):
        data = self.cleaned_data['transaction_date']
        if data < datetime.date(year=2024, month=6, day=25):
            raise ValidationError(_('Вы указали дату до смены.'))
        if data > datetime.date(year=2024, month=6, day=25) + datetime.timedelta(weeks=3):
            raise ValidationError(_('Вы указали дату после смены.'))
        return data
    
    list_accounts = account.objects.exclude(party=0)
    transaction_receiver = forms.ModelChoiceField(queryset=list_accounts, label="Получатель:")#, widget=forms.RadioSelect()) 
    
    def clean_transaction_receiver(self):
            return self.cleaned_data['transaction_receiver']
    
    #ВНИМАНИЕ!!! Если не получается сделать миграцию, закомментируйте следующие пять строк кода на время миграции.
    #После успешной миграции не забудьте откомментировать строки!
    not_list_accounts = list(account.objects.filter(party=0).exclude(last_name='Admin'))
    list_accounts = account.objects.all()
    for i in not_list_accounts:
        list_accounts = list_accounts.exclude(id=i.id)
    transaction_creator = forms.ModelChoiceField(queryset=list_accounts, label="Даватель:")#, widget=forms.RadioSelect()) 
    
    def clean_transaction_creator(self):
            return self.cleaned_data['transaction_creator']
    
    transaction_history = forms.ModelChoiceField(queryset=account.objects.all(), label="Создатель:")#, widget=forms.RadioSelect()) 
    
    def clean_transaction_history(self):
            return self.cleaned_data['transaction_history']

    transaction_cnt = forms.FloatField(help_text="Укажите сумму перевода.", label="Сумма:")

    def clean_transaction_cnt(self):
        cnt = self.cleaned_data['transaction_cnt']
        if cnt <= 0:
            raise ValidationError(_('Вы не можете ввести сумму средств меньше нуля или ноль.'))
        return cnt

    transaction_comment = forms.CharField(help_text="Пояснение начисления/штрафа.", label="Комментарий:")

    def clean_transaction_comment(self):
        return self.cleaned_data['transaction_comment']
    
    transaction_sign = forms.ChoiceField(choices=transaction.SIGN_SET, help_text="Выберите тип: премия/штраф", label="Тип транзакции:")
    
    def clean_transaction_sign(self):
            return self.cleaned_data['transaction_sign']
    
    class Meta:
        model = transaction
        fields = ['transaction_date', 'transaction_receiver', 'transaction_cnt', 'transaction_comment', 'transaction_sign']

class NewTransactionBuyForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(NewTransactionBuyForm, self).__init__(*args, **kwargs)
        goods = shop.objects.all()
        for good in goods:
            self.fields[f"good_{good.id}"] = forms.IntegerField(label=good.name, initial=0)

    def clean_goods(self):
        cleaned_data = super().clean()
        dt = {}
        ls = []
        for field_name, value in cleaned_data.items():
            if field_name.startswith('good_'):
                good_id = field_name.split('_')[1]
                good = shop.objects.get(id=good_id)
                dt[good] = value
                ls.append(uuid.UUID(good_id))
        return [dt, ls]
    
    list_accounts = account.objects.exclude(party=0)
    transaction_receiver = forms.ModelChoiceField(queryset=list_accounts, label="Покупатель:")#, widget=forms.RadioSelect()) 
    
    def clean_transaction_receiver(self):
            return self.cleaned_data['transaction_receiver']
    
class ReNewTransactionStaffForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['delete'] = forms.BooleanField(required=False, widget=forms.HiddenInput())
        self.fields['edit'] = forms.BooleanField(required=False, widget=forms.HiddenInput())
    
    transaction_history = forms.ModelChoiceField(queryset=account.objects.all(), label="Создатель:")#, widget=forms.RadioSelect()) 
    
    def clean_transaction_receiver(self):
            return self.cleaned_data['transaction_history']

    transaction_date = forms.DateField(help_text="Дата должна быть в пределах смены, по умолчанию сегодня.", label="Дата:")

    def clean_transaction_date(self):
        data = self.cleaned_data['transaction_date']
        if data < datetime.date(year=2024, month=6, day=25):
            raise ValidationError(_('Вы указали дату до смены.'))
        if data > datetime.date(year=2024, month=6, day=25) + datetime.timedelta(weeks=3):
            raise ValidationError(_('Вы указали дату после смены.'))
        return data

    transaction_cnt = forms.FloatField(help_text="Укажите сумму перевода.", label="Сумма:")

    def clean_transaction_cnt(self):
        cnt = self.cleaned_data['transaction_cnt']
        if cnt <= 0:
            raise ValidationError(_('Вы не можете ввести сумму средств меньше нуля или ноль.'))
        return cnt

    transaction_comment = forms.CharField(help_text="Пояснение начисления/штрафа.", label="Комментарий:")

    def clean_transaction_comment(self):
        return self.cleaned_data['transaction_comment']
    
    transaction_sign = forms.ChoiceField(choices=transaction.SIGN_SET, help_text="Выберите тип: премия/штраф", label="Тип транзакции:")
    
    def clean_transaction_sign(self):
            return self.cleaned_data['transaction_sign']

class NewTransactionBaseForm(forms.Form):
    transaction_receiver = forms.ModelChoiceField(queryset=account.objects.exclude(party=0).order_by('party', 'last_name'), label="Получатель:")

    def clean_transaction_receiver(self):
        return self.cleaned_data['transaction_receiver']

    transaction_cnt = forms.FloatField(help_text="Укажите сумму перевода.", label="Сумма:")

    def clean_transaction_cnt(self):
        cnt = self.cleaned_data['transaction_cnt']
        if cnt <= 0:
            raise ValidationError(_('Вы не можете перевести сумму средств меньше нуля или ноль.'))
        return cnt

    transaction_comment = forms.CharField(help_text="Пояснение начисления/штрафа.", label="Комментарий:")

    def clean_transaction_comment(self):
        return self.cleaned_data['transaction_comment']
    
    class Meta:
        model = transaction
        fields = ['transaction_date', 'transaction_receiver', 'transaction_cnt', 'transaction_comment']

class NewMessageForm(forms.Form):
    message_text = forms.CharField(widget=forms.Textarea, help_text="Текст сообщения.", label="Текст:")

    def clean_message_text(self):
        return self.cleaned_data['message_text']

    message_anonim = forms.BooleanField(initial=False, required=False, label="Анонимно?", help_text="Если вы хотите отправить сообщение анонимно, вы должны поставить галочку.")

    def clean_message_anonim(self):
        return self.cleaned_data['message_anonim']
    
    class Meta:
        model = message
        fields = ['message_receiver', 'message_text', 'message_anonim']

class NewMessageForm_WithoutAnonim(forms.Form):
    message_text = forms.CharField(widget=forms.Textarea, help_text="Текст сообщения.", label="Текст:")

    def clean_message_text(self):
        return self.cleaned_data['message_text']
    
    class Meta:
        model = message
        fields = ['message_receiver', 'message_text', 'message_anonim']

class ReNewMessageFormAnonim(forms.Form):
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['delete'] = forms.BooleanField(required=False, widget=forms.HiddenInput())

    message_text = forms.CharField(widget=forms.Textarea, help_text="Текст сообщения.", label="Текст:")

    def clean_message_text(self):
        return self.cleaned_data['message_text']

    message_anonim = forms.BooleanField(initial=False, required=False, label="Анонимно?", help_text="Если вы хотите отправить сообщение анонимно, вы должны поставить галочку.")

    def clean_message_anonim(self):
        return self.cleaned_data['message_anonim']
    
    class Meta:
        model = message
        fields = ['message_text', 'message_anonim']

class ReNewMessageFormBase(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['delete'] = forms.BooleanField(required=False, widget=forms.HiddenInput())

    message_text = forms.CharField(widget=forms.Textarea, help_text="Текст сообщения.", label="Текст:")

    def clean_message_text(self):
        return self.cleaned_data['message_text']
    
    class Meta:
        model = message
        fields = ['message_text']

class NewChatForm(forms.Form):
    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('current_user', None)
        super(NewChatForm, self).__init__(*args, **kwargs)
        if current_user is not None:
            self.fields['chat_members'].queryset = account.objects.exclude(pk=current_user.pk)

    chat_name = forms.CharField(label="Название чата:")

    def clean_chat_name(self):
        name = self.cleaned_data['chat_name']
        chat_all = [f'{i.name}' for i in chat.objects.all() if chat_valid.objects.get(what_chat=i).avaliable]
        if f'{name}' in chat_all: raise ValidationError(_('Чат с таким именем уже существует. Постарайтесь быть креативнее.'))
        return name
    
    chat_description = forms.CharField(label="Описание чата:")

    def clean_chat_description(self):
        return self.cleaned_data['chat_description']
    
    chat_anonim = forms.BooleanField(initial=False, required=False, help_text="Если вы хотите сделать чат анонимным, поставьте здесь галочку.\nЭтот параметр неизменяем.", label="Чат анонимный?")

    def clean_chat_anonim(self):
        return self.cleaned_data['chat_anonim']

    chat_anonim_legacy = forms.BooleanField(initial=False, required=False, label="Анонимные сообщения?", help_text="Если вы хотите разрешить отправку анонимных сообщений, вы должны поставить галочку.\nЭтот параметр неизменяем, не влияет на анонимный чат.")

    def clean_chat_anonim_legacy(self):
        return self.cleaned_data['chat_anonim_legacy']

    chat_members = forms.ModelMultipleChoiceField(queryset=account.objects.all(), label="Участники чата:", help_text="Выберите участников чата. (Вы будете в нём независимо от вашего выбора здесь.)")

    def clean_chat_members(self):
        return self.cleaned_data['chat_members']

class NewChatFormConflict(forms.Form):
    CONFLICT_SOLVES = (
        (0, "Создать новый чат и заархивировать существующий"),
        (1, "Не создавать новый чат, заархивировать существующий"),
        (2, "Не создавать новый чат, не архивировать существующий"),
    )

    solve = forms.ChoiceField(choices=CONFLICT_SOLVES, label="Действие:")

    def clean_type_(self):
        return self.cleaned_data['solve']

class ReNewChatFormAnonim(forms.Form):
    def __init__(self, *args, **kwargs):
        current_users = kwargs.pop('current_users', None)
        current_user = kwargs.pop('current_user', None)
        super(ReNewChatFormAnonim, self).__init__(*args, **kwargs)
        if current_users is not None:
            current_users_pk = [i.pk for i in current_users]
            self.fields['chat_creator'].queryset = account.objects.filter(pk__in=current_users_pk)
            if current_user is not None: self.fields['chat_creator'].queryset = account.objects.filter(pk__in=current_users_pk).exclude(pk=current_user.pk)
        self.fields['delete'] = forms.BooleanField(required=False, widget=forms.HiddenInput())

    chat_creator = forms.ModelChoiceField(queryset=account.objects.all(), required=False, label="Создатель:", help_text="Здесь вы можете изменить создателя чата. Это необязательно.")

    def clean_chat_creator(self):
        return self.cleaned_data['chat_creator']

    chat_name = forms.CharField(label="Название чата:")

    def clean_chat_name(self):
        name = self.cleaned_data['chat_name']
        #chat_all = [f'{i.name}' for i in chat.objects.all() if chat_valid.objects.get(what_chat=i).avaliable]
        #if f'{name}' in chat_all: raise ValidationError(_('Чат с таким именем уже существует. Постарайтесь быть креативнее.'))
        return name

    chat_text = forms.CharField(widget=forms.Textarea, label="Описание чата:")

    def clean_chat_text(self):
        return self.cleaned_data['chat_text']

    chat_anonim = forms.BooleanField(required=False, label="Анонимные сообщения?", help_text="Если вы хотите разрешить отправку сообщения анонимно, вы должны поставить галочку.")

    def clean_message_anonim(self):
        return self.cleaned_data['chat_anonim']

class ReNewChatFormBase(forms.Form):
    def __init__(self, *args, **kwargs):
        current_users = kwargs.pop('current_users', None)
        current_user = kwargs.pop('current_user', None)
        super(ReNewChatFormBase, self).__init__(*args, **kwargs)
        if current_users is not None:
            current_users_pk = [i.pk for i in current_users]
            self.fields['chat_creator'].queryset = account.objects.filter(pk__in=current_users_pk)
            if current_user is not None: self.fields['chat_creator'].queryset = account.objects.filter(pk__in=current_users_pk).exclude(pk=current_user.pk)
        self.fields['delete'] = forms.BooleanField(required=False, widget=forms.HiddenInput())

    chat_creator = forms.ModelChoiceField(queryset=account.objects.all(), required=False, label="Создатель:", help_text="Здесь вы можете изменить создателя чата. Это необязательно.")

    def clean_chat_creator(self):
        return self.cleaned_data['chat_creator']

    chat_name = forms.CharField(label="Название чата:")

    def clean_chat_name(self):
        name = self.cleaned_data['chat_name']
        #chat_all = [f'{i.name}' for i in chat.objects.all() if chat_valid.objects.get(what_chat=i).avaliable]
        #if f'{name}' in chat_all: raise ValidationError(_('Чат с таким именем уже существует. Постарайтесь быть креативнее.'))
        return name

    chat_text = forms.CharField(widget=forms.Textarea, label="Описание чата:")

    def clean_chat_text(self):
        return self.cleaned_data['chat_text']

class NewAccountForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['save_and_new'] = forms.BooleanField(required=False, widget=forms.HiddenInput())

    EXISTING_TYPES = (
        (0, "Пионер"),
        (1, "Педсостав"),
    )

    type_ = forms.ChoiceField(choices=EXISTING_TYPES, label="Тип аккаунта:")

    def clean_type_(self):
        return self.cleaned_data['type_']

    first_name = forms.CharField(label="Имя:")

    def clean_first_name(self):
        return self.cleaned_data['first_name']
    
    middle_name = forms.CharField(label="Отчество:")

    def clean_middle_name(self):
        return self.cleaned_data['middle_name']
    
    last_name = forms.CharField(label="Фамилия:")

    def clean_last_name(self):
        return self.cleaned_data['last_name']

    user_group = forms.ChoiceField(choices=account.EXISTING_GROUPS, label="Группа занятий:")

    def clean_user_group(self):
        return self.cleaned_data['user_group']

    party = forms.IntegerField(label="Номер отряда:")

    def clean_party(self):
        return self.cleaned_data['party']

class NewAccountFullForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['save_and_new'] = forms.BooleanField(required=False, widget=forms.HiddenInput())

    EXISTING_TYPES = (
        (0, "Пионер"),
        (1, "Педсостав"),
    )

    type_ = forms.ChoiceField(choices=EXISTING_TYPES, label="Тип аккаунта:")

    def clean_type_(self):
        return self.cleaned_data['type_']

    first_name = forms.CharField(label="Имя:")

    def clean_first_name(self):
        return self.cleaned_data['first_name']
    
    middle_name = forms.CharField(label="Отчество:")

    def clean_middle_name(self):
        return self.cleaned_data['middle_name']
    
    last_name = forms.CharField(label="Фамилия:")

    def clean_last_name(self):
        return self.cleaned_data['last_name']
    
    username = forms.CharField(label="Login:")

    def clean_username(self):
        return self.cleaned_data['username']
    
    password = forms.CharField(label="Password:")

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) != 8 and len(password) != 12:
            raise ValidationError(_('Длина пароля должна быть равной 8-ми символам для пионера и 12-ти символам для педагога.'))
        return password

    user_group = forms.ChoiceField(choices=account.EXISTING_GROUPS, label="Группа занятий:")

    def clean_user_group(self):
        return self.cleaned_data['user_group']

    party = forms.IntegerField(label="Номер отряда:")

    def clean_party(self):
        return self.cleaned_data['party']

class ReNewAccountForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['delete'] = forms.BooleanField(required=False, widget=forms.HiddenInput())

    first_name = forms.CharField(label="Имя:")

    def clean_first_name(self):
        return self.cleaned_data['first_name']
    
    middle_name = forms.CharField(label="Отчество:")

    def clean_middle_name(self):
        return self.cleaned_data['middle_name']
    
    last_name = forms.CharField(label="Фамилия:")

    def clean_last_name(self):
        return self.cleaned_data['last_name']
    
    balance = forms.IntegerField(label="Баланс:")

    def clear_balance(self):
        return self.cleaned_data['balance']

    username = forms.CharField(label="Login:")

    def clean_username(self):
        return self.cleaned_data['username']

    user_group = forms.ChoiceField(choices=account.EXISTING_GROUPS, label="Группа занятий:")

    def clean_user_group(self):
        return self.cleaned_data['user_group']

    party = forms.IntegerField(label="Номер отряда:")

    def clean_party(self):
        return self.cleaned_data['party']

class NewPlanAddForm(forms.Form):
    time = forms.CharField(max_length=40, label="Во сколько:")

    def clean_time(self):
        return self.cleaned_data["time"]

    comment = forms.CharField(label="Комментарий:")

    def clean_comment(self):
        return self.cleaned_data["comment"]

    number = forms.IntegerField(label="Номер в списке:")

    def clean_number(self):
        return int(self.cleaned_data["number"])

class ReNewPlanAddForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['delete'] = forms.BooleanField(required=False, widget=forms.HiddenInput())
    
    time = forms.CharField(max_length=40, label="Во сколько:")

    def clean_time(self):
        return self.cleaned_data["time"]

    comment = forms.CharField(label="Комментарий:")

    def clean_comment(self):
        return self.cleaned_data["comment"]

    number = forms.IntegerField(label="Номер в списке:")

    def clean_number(self):
        return int(self.cleaned_data["number"])

class NewShopAddForm(forms.Form):
    name = forms.CharField(max_length=40, label="Название:")

    def clean_name(self):
        return self.cleaned_data["name"]

    comment = forms.CharField(label="Комментарий:")

    def clean_comment(self):
        return self.cleaned_data["comment"]

    cost = forms.IntegerField(label="Цена:")

    def clean_cost(self):
        return int(self.cleaned_data["cost"])

class ReNewShopAddForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['delete'] = forms.BooleanField(required=False, widget=forms.HiddenInput())
    
    name = forms.CharField(max_length=40, label="Название:")

    def clean_name(self):
        return self.cleaned_data["name"]

    comment = forms.CharField(label="Комментарий:")

    def clean_comment(self):
        return self.cleaned_data["comment"]

    cost = forms.IntegerField(label="Цена:")

    def clean_cost(self):
        return int(self.cleaned_data["cost"])

class NewDailyAnswerAddForm(forms.Form):
    name = forms.CharField(max_length=40, label="Название задачи:")

    def clean_name(self):
        return self.cleaned_data["name"]

    comment = forms.CharField(label="Условие задачи:")

    def clean_comment(self):
        return self.cleaned_data["comment"]

    cost = forms.IntegerField(label="Награда:")

    def clean_cost(self):
        return int(self.cleaned_data["cost"])

    giga_ans = forms.BooleanField(label="Это задача смены?", initial=False, required=False)

    def clean_giga_ans(self):
        return int(self.cleaned_data["giga_ans"])

class ReNewDailyAnswerAddForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['delete'] = forms.BooleanField(required=False, widget=forms.HiddenInput())
    
    name = forms.CharField(max_length=40, label="Название задачи:")

    def clean_name(self):
        return self.cleaned_data["name"]

    comment = forms.CharField(label="Условие задачи:")

    def clean_comment(self):
        return self.cleaned_data["comment"]

    cost = forms.IntegerField(label="Награда:")

    def clean_cost(self):
        return int(self.cleaned_data["cost"])

    giga_ans = forms.BooleanField(label="Это задача смены?", required=False)

    def clean_giga_ans(self):
        return int(self.cleaned_data["giga_ans"])
