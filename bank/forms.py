from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from bank.models import account, transaction
import datetime

class NewTransactionStaffForm(forms.Form):
    transaction_date = forms.DateField(help_text="Дата должна быть в пределах смены, по умолчанию сегодня.")

    def clean_transaction_date(self):
        data = self.cleaned_data['transaction_date']
        if data < datetime.date(year=2023, month=6, day=25):
            raise ValidationError(_('Вы указали дату до смены.'))
        if data > datetime.date(year=2023, month=6, day=25) + datetime.timedelta(weeks=3):
            raise ValidationError(_('Вы указали дату после смены.'))
        return data
    
    transaction_receiver = forms.ModelChoiceField(queryset=account.objects.all())
    
    def clean_transaction_receiver(self):
            return self.cleaned_data['transaction_receiver']

    transaction_cnt = forms.FloatField(help_text="Укажите сумму перевода.")

    def clean_transaction_cnt(self):
        cnt = self.cleaned_data['transaction_cnt']
        if cnt <= 0:
            raise ValidationError(_('Вы не можете ввести сумму средств менее нуля.'))
        return cnt

    transaction_comment = forms.CharField(help_text="Пояснение начисления/штрафа.")

    def clean_transaction_comment(self):
        return self.cleaned_data['transaction_comment']
    
    transaction_sign = forms.ChoiceField(choices=transaction.SIGN_SET, help_text="Выберите тип: премия/штраф")
    
    def clean_transaction_sign(self):
            return self.cleaned_data['transaction_sign']
    
    class Meta:
        model = transaction
        fields = ['transaction_date', 'transaction_receiver', 'transaction_cnt', 'transaction_comment', 'transaction_sign']
    
class NewTransactionBaseForm(forms.Form):
    transaction_date = forms.DateField(help_text="Дата должна быть в пределах смены, по умолчанию сегодня.")

    def clean_transaction_date(self):
        data = self.cleaned_data['transaction_date']
        if data < datetime.date(year=2023, month=6, day=25):
            raise ValidationError(_('Вы указали дату до смены.'))
        if data > datetime.date(year=2023, month=6, day=25) + datetime.timedelta(weeks=3):
            raise ValidationError(_('Вы указали дату после смены.'))
        return data
    
    transaction_receiver = forms.ModelChoiceField(queryset=account.objects.all())

    def clean_transaction_receiver(self):
        return self.cleaned_data['transaction_receiver']

    transaction_cnt = forms.FloatField(help_text="Укажите сумму перевода.")

    def clean_transaction_cnt(self):
        cnt = self.cleaned_data['transaction_cnt']
        if cnt <= 0:
            raise ValidationError(_('Вы не можете перевести сумму средств менее нуля.'))
        return cnt

    transaction_comment = forms.CharField(help_text="Пояснение начисления/штрафа.")

    def clean_transaction_comment(self):
        return self.cleaned_data['transaction_comment']
    
    class Meta:
        model = transaction
        fields = ['transaction_date', 'transaction_receiver', 'transaction_cnt', 'transaction_comment']
