from django.shortcuts import render
from bank.models import account, transaction, rule_u, rule_a, rule_t, rule_p, shop
from django.views import generic
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from bank.forms import NewTransactionStaffForm, NewTransactionBaseForm
from django.contrib.auth.decorators import permission_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
import datetime

def index(request):
    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1
    return render(
        request,
        'index.html',
        context={'num_visits': num_visits},
    )

@permission_required('bank.shop')
def shop_view(request):
    return render(
        request,
        'bank/shop.html',
        context={'goods': shop.objects.all()}
    )

def rules(request):
    return render(
        request,
        'bank/rules.html',
        context={
            'rule_u': rule_u.objects.order_by('num_pt1', 'num_pt2'),
            'rule_a': rule_a.objects.order_by('num_pt1', 'num_pt2'),
            'rule_t': rule_t.objects.order_by('num_pt1', 'num_pt2'),
            'rule_p': rule_p.objects.order_by('num_pt1', 'num_pt2'),
        }
    )

@permission_required('bank.staff_')
def info_for_staff(request):
    return render(
        request,
        'bank/info_staff.html'
    )

class TransactionsListView(PermissionRequiredMixin, generic.ListView):
    permission_required = ('bank.staff_', 'bank.viewer',)
    model = account
    template_name ='bank/balances.html'
    paginate_by = 20

    def get_queryset(self):
        return account.objects.order_by('party') #.filter(name=self.request.user.account.balance)

class TransactionsDetailView(PermissionRequiredMixin, generic.DetailView):
    permission_required = ('bank.staff_', 'bank.viewer',)
    model = account
    template_name ='bank/transactions_detail.html'
    paginate_by = 20

    def get_queryset(self):
        return account.objects.all()

class MyTransactionsView(LoginRequiredMixin, generic.ListView):
    model = transaction
    template_name ='bank/my_transactions.html'
    paginate_by = 20

    def get_queryset(self):
        return transaction.objects.all()

@permission_required('bank.staff_')
def new_transaction_staff_add(request):
    if request.method == 'POST':
        form = NewTransactionStaffForm(request.POST)
        if form.is_valid():
            new_transaction = transaction()
            new_transaction.date = form.cleaned_data['transaction_date']
            new_transaction.comment = form.cleaned_data['transaction_comment']
            new_transaction.creator = account.objects.get(last_name='Admin')
            new_transaction.receiver = form.cleaned_data['transaction_receiver']
            new_transaction.sign = form.cleaned_data['transaction_sign']
            if new_transaction.creator == new_transaction.receiver:
                return HttpResponse("<h2>Вы не можете перевести деньги на банковский счёт. <a href=\"/\">Назад...</a></h2>")
            new_transaction.cnt = form.cleaned_data['transaction_cnt']
            new_transaction.save()
            return HttpResponse("<h2>Вы успешно добавили транзакцию. <a href=\"/\">Назад...</a></h2>")
    else:
        transaction_date = datetime.datetime.now()
        transaction_comment = "Не указано"
        transaction_cnt = 0
        transaction_sign = '-'
        form = NewTransactionBaseForm(initial={'transaction_date': transaction_date, 'transaction_comment': transaction_comment,
                                               'transaction_cnt': transaction_cnt, 'transaction_sign': transaction_sign})

    return render(request, 'bank/transaction_form_staff.html', {'form': form,})

def new_transaction_base_add(request):
    if request.method == 'POST':
        form = NewTransactionBaseForm(request.POST)
        if form.is_valid():
            new_transaction = transaction()
            new_transaction.date = form.cleaned_data['transaction_date']
            new_transaction.comment = form.cleaned_data['transaction_comment']
            new_transaction.creator = request.user.account
            new_transaction.receiver = form.cleaned_data['transaction_receiver']
            if new_transaction.creator == new_transaction.receiver:
                return HttpResponse("<h2>Вы не можете перевести деньги на свой счёт. <a href=\"/\">Назад...</a></h2>")
            elif account.objects.get(last_name='Admin') == new_transaction.receiver:
                return HttpResponse("<h2>Вы не можете перевести деньги на банковский счёт. <a href=\"/\">Назад...</a></h2>")
            new_transaction.cnt = form.cleaned_data['transaction_cnt']
            if new_transaction.cnt > request.user.account.balance:
                return HttpResponse("<h2>Вы не можете перевести денег больше, чем у вас есть. <a href=\"/\">Назад...</a>    </h2>")
            new_transaction.save()
            return HttpResponse("<h2>Вы успешно добавили транзакцию. <a href=\"/\">Назад...</a></h2>")
    else:
        transaction_date = datetime.datetime.now()
        transaction_comment = "Не указано"
        transaction_cnt = 0
        form = NewTransactionBaseForm(initial={'transaction_date': transaction_date, 'transaction_comment': transaction_comment, 'transaction_cnt': transaction_cnt})

    return render(request, 'bank/transaction_form.html', {'form': form,})
