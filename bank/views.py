from django.shortcuts import redirect, render
from bank.models import account, transaction, shop, plan, message, daily_answer, rools, chat, chat_valid, chat_and_acc
from django.views import generic
from django.contrib.auth.models import User, Group, Permission, AnonymousUser
from django.contrib.auth.hashers import make_password
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from bank.forms import NewTransactionStaffForm, NewTransactionBaseForm, NewMessageForm, NewAccountForm, ReNewMessageFormAnonim,\
    ReNewMessageFormBase, NewChatForm, NewMessageForm_WithoutAnonim, ReNewChatFormAnonim, ReNewChatFormBase, SetStatus,\
        SetReadStatusForm, NewChatFormConflict, ReNewTransactionStaffForm, NewTransactionBuyForm, NewTransactionFullForm,\
            NewAccountFullForm, ReNewAccountForm, NewTransactionStaffFormParty, NewPlanAddForm, ReNewPlanAddForm,\
                NewShopAddForm, ReNewShopAddForm, NewDailyAnswerAddForm, ReNewDailyAnswerAddForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import permission_required, login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models import Q, Subquery
import datetime
import random
import string
import uuid

def index(request):
    forbes = account.objects.exclude(party=0).order_by('-balance')[:10]
    antiforbes = account.objects.exclude(party=0).order_by('balance')[:3]
    admin = account.objects.get(last_name="Admin")
    readen_status = True
    if request.user == AnonymousUser:
        for i in list(chat_and_acc.objects.filter(what_acc=request.user.account)):
            readen_status &= i.readen
    return render(
        request,
        'index.html',
        context={'forbes': forbes, 'antiforbes': antiforbes, 'admin': admin, 'readen_status': readen_status,},
    )

def plan_x(request):
    return render(
        request,
        'bank/plan.html',
        context={'plan': plan.objects.all(),},
    )

@login_required
def home(request):
    chat_valid_all = list(chat_valid.objects.exclude(avaliable=False))
    list_id_chats = []
    for i in chat_valid_all:
        if i.getting_access(request.user.account):
            list_id_chats.append(i.what_chat.id)
    mess_pr = chat.objects.filter(id__in=list_id_chats)
    chat_and_acc_all = chat_and_acc.objects.filter(what_chat__in=mess_pr).filter(what_acc=request.user.account)
    mess_pub = message.objects.filter(receiver=None)
    paginator1 = Paginator(mess_pr, 25)
    paginator2 = Paginator(mess_pub, 10)
    page1 = request.GET.get('page1')
    page2 = request.GET.get('page2')
    try:
        items1 = paginator1.page(page1)
    except PageNotAnInteger:
        items1 = paginator1.page(1)
    except EmptyPage:
        items1 = paginator1.page(paginator1.num_pages)
    try:
        items2 = paginator2.page(page2)
    except PageNotAnInteger:
        items2 = paginator2.page(1)
    except EmptyPage:
        items2 = paginator2.page(paginator2.num_pages)
    if request.method == 'POST':
        form = SetStatus(request.POST)
        if form.is_valid():
            account_ = account.objects.get(id=request.user.account.id)
            new_status = form.cleaned_data['status']
            account_.account_status = new_status
            account_.save()
            return redirect('messages')
    else:
        status = request.user.account.account_status
        form = SetStatus(initial={'status': status,})
    context={'messages': mess_pr, 'messages_public': mess_pub, 'items1': items1, 'items2': items2, 'form': form, 'readen_status': chat_and_acc_all,}
    return render(
        request,
        'bank/messages.html',
        context=context,
    )

@login_required
def home_send(request):
    mess_pr = message.objects.filter(creator=request.user.account).exclude(receiver=None)
    mess_pr_ = message.objects.filter(creator=request.user.account).exclude(receiver=None)
    if list(mess_pr) != []:
        print(mess_pr)
        i = 0
        while True:
            if not chat_valid.objects.get(what_chat=mess_pr[i].receiver).avaliable:
                mess_pr = mess_pr.exclude(id=mess_pr[i].id)
                i -= 1
            i += 1
            if i >= len(mess_pr): break
    if list(mess_pr_) != []:
        i = 0
        while True:
            if chat_valid.objects.get(what_chat=mess_pr_[i].receiver).avaliable:
                mess_pr_ = mess_pr_.exclude(id=mess_pr_[i].id)
                i -= 1
            i += 1
            if i >= len(mess_pr_): break
    mess_pub = message.objects.filter(creator=request.user.account).filter(receiver=None)
    paginator1 = Paginator(mess_pr, 25)
    paginator2 = Paginator(mess_pub, 25)
    paginator3 = Paginator(mess_pr_, 25)
    page1 = request.GET.get('page1')
    page2 = request.GET.get('page2')
    page3 = request.GET.get('page2')
    try:
        items1 = paginator1.page(page1)
    except PageNotAnInteger:
        items1 = paginator1.page(1)
    except EmptyPage:
        items1 = paginator1.page(paginator1.num_pages)
    try:
        items2 = paginator2.page(page2)
    except PageNotAnInteger:
        items2 = paginator2.page(1)
    except EmptyPage:
        items2 = paginator2.page(paginator2.num_pages)
    try:
        items3 = paginator3.page(page3)
    except PageNotAnInteger:
        items3 = paginator3.page(1)
    except EmptyPage:
        items3 = paginator3.page(paginator3.num_pages)
    return render(
        request,
        'bank/messages_list.html',
        context={'messages': mess_pr, 'messages_public': mess_pub,
                 'items1': items1, 'items2': items2, 'items3': items3,},
    )

def shop_view(request):
    return render(
        request,
        'bank/shop.html',
        context={'goods': shop.objects.all()}
    )

def rools_view(request):
    return render(
        request,
        'bank/rules.html',
        context={
            'rool_u': rools.objects.filter(num_type='УкТ').order_by('num_pt1', 'num_pt2'),
            'rool_a': rools.objects.filter(num_type='АкТ').order_by('num_pt1', 'num_pt2'),
            'rool_t': rools.objects.filter(num_type='ТкТ').order_by('num_pt1', 'num_pt2'),
            'rool_p': rools.objects.filter(num_type='КпТ').order_by('num_pt1', 'num_pt2'),
        }
    )

@permission_required('bank.staff_')
@permission_required('bank.edit_users')
def account_info(request):
    acc_all = account.objects.all()
    paginator1 = Paginator(acc_all, 25)
    page1 = request.GET.get('page1')
    try:
        items1 = paginator1.page(page1)
    except PageNotAnInteger:
        items1 = paginator1.page(1)
    except EmptyPage:
        items1 = paginator1.page(paginator1.num_pages)
    return render(
        request,
        'bank/account_status.html',
        context={
            'object_list': items1,
        }
    )

def answers(request):
    return render(
        request,
        'bank/answers.html',
        context={'answers': daily_answer.objects.all(),}
    )

class TransactionsListView(PermissionRequiredMixin, generic.ListView):
    permission_required = ('bank.staff_',)
    model = account
    template_name ='bank/balances.html'
    paginate_by = 20

    def get_queryset(self):
        return account.objects.exclude(party=0).exclude(last_name = 'party1').exclude(last_name = 'party2').exclude(last_name = 'party3').exclude(last_name = 'party4').order_by('party', 'last_name') #.filter(name=self.request.user.account.balance)

class TransactionsDetailView(PermissionRequiredMixin, generic.DetailView):
    permission_required = ('bank.staff_',)
    model = account
    template_name ='bank/transactions_detail.html'

    def get_queryset(self):
        return account.objects.all()

class AllTransactionsListView(PermissionRequiredMixin, generic.ListView):
    permission_required = ('bank.staff_', 'bank.transaction')
    model = transaction
    template_name ='bank/transaction_status.html'
    paginate_by = 20

    def get_queryset(self):
        return transaction.objects.order_by('counted', '-date', 'receiver', 'history', 'cnt') #.filter(name=self.request.user.account.balance)

class MyTransactionsView(LoginRequiredMixin, generic.ListView):
    model = transaction
    template_name ='bank/my_transactions.html'

    def get_queryset(self):
        return transaction.objects.all()

@permission_required('bank.staff_')
@permission_required('bank.transaction')
def new_transaction_staff_add(request):
    if request.method == 'POST':
        form = NewTransactionStaffForm(request.POST)
        if form.is_valid():
            new_transaction = transaction()
            new_transaction.id = uuid.uuid4()
            new_transaction.date = form.cleaned_data['transaction_date']
            new_transaction.comment = form.cleaned_data['transaction_comment']
            new_transaction.creator = account.objects.get(last_name='Admin')
            new_transaction.receiver = form.cleaned_data['transaction_receiver']
            new_transaction.sign = form.cleaned_data['transaction_sign']
            new_transaction.history = request.user.account
            if new_transaction.creator == new_transaction.receiver:
                return HttpResponse("<h2>Вы не можете перевести деньги на свой счёт. <a href=\"/\">Назад...</a></h2>")
            new_transaction.cnt = form.cleaned_data['transaction_cnt']
            new_transaction.save()
            new_transaction.count()
            return redirect('info-staff')
    else:
        transaction_date = datetime.datetime.now()
        transaction_comment = "Не указано"
        transaction_cnt = 0
        transaction_sign = '+'
        form = NewTransactionStaffForm(initial={'transaction_date': transaction_date, 'transaction_comment': transaction_comment,
                                               'transaction_cnt': transaction_cnt, 'transaction_sign': transaction_sign})

    return render(request, 'bank/transaction_form_staff.html', {'form': form,})

@permission_required('bank.staff_')
@permission_required('bank.transaction')
def new_transaction_staff_party_add(request):
    not_list_accounts = list(account.objects.filter(party=0).exclude(last_name='Admin'))
    list_accounts = []
    for i in not_list_accounts:
        list_accounts.append(i.id)
    if request.method == 'POST':
        form = NewTransactionStaffFormParty(request.POST, current_users=list_accounts)
        if form.is_valid():
            receiver = int(form.cleaned_data['transaction_receiver'])
            all_receivers = account.objects.filter(party=receiver)
            for i in all_receivers:
                new_transaction = transaction()
                new_transaction.id = uuid.uuid4()
                new_transaction.date = form.cleaned_data['transaction_date']
                new_transaction.comment = form.cleaned_data['transaction_comment']
                new_transaction.creator = account.objects.get(last_name='Admin')
                new_transaction.receiver = i
                new_transaction.sign = form.cleaned_data['transaction_sign']
                new_transaction.history = request.user.account
                new_transaction.cnt = form.cleaned_data['transaction_cnt']
                new_transaction.save()
                new_transaction.count()
            return redirect('info-staff')
    else:
        transaction_date = datetime.datetime.now()
        transaction_comment = "Не указано"
        transaction_cnt = 0
        transaction_sign = '+'
        form = NewTransactionStaffFormParty(initial={'transaction_date': transaction_date, 'transaction_comment': transaction_comment,
               'transaction_cnt': transaction_cnt, 'transaction_sign': transaction_sign}, current_users=list_accounts,)

    return render(request, 'bank/transaction_form_staff_party.html', {'form': form,})

@permission_required('bank.staff_')
@permission_required('bank.transaction')
def new_transaction_full_add(request):
    if request.method == 'POST':
        form = NewTransactionFullForm(request.POST)
        if form.is_valid():
            new_transaction = transaction()
            new_transaction.id = uuid.uuid4()
            new_transaction.date = form.cleaned_data['transaction_date']
            new_transaction.comment = form.cleaned_data['transaction_comment']
            new_transaction.creator = form.cleaned_data['transaction_creator']
            new_transaction.history = form.cleaned_data['transaction_history']
            new_transaction.receiver = form.cleaned_data['transaction_receiver']
            new_transaction.sign = form.cleaned_data['transaction_sign']
            if new_transaction.creator == new_transaction.receiver:
                return HttpResponse("<h2>Неужели вы <em>настолько</em> жадина? <a href=\"/\">Назад...</a></h2>")
            elif account.objects.get(last_name='Admin') == new_transaction.receiver:
                return HttpResponse("<h2>Вы не можете перевести деньги на банковский счёт. Сегодня без донатов. <a href=\"/\">Назад...</a></h2>")
            new_transaction.cnt = form.cleaned_data['transaction_cnt']
            new_transaction.save()
            new_transaction.count()
            return redirect('info-staff')
    else:
        transaction_date = datetime.datetime.now()
        transaction_comment = "Не указано"
        transaction_cnt = 0
        transaction_sign = '+'
        form = NewTransactionFullForm(initial={'transaction_date': transaction_date, 'transaction_comment': transaction_comment,
                                               'transaction_cnt': transaction_cnt, 'transaction_sign': transaction_sign})

    return render(request, 'bank/transaction_form_full.html', {'form': form,})

@permission_required('bank.staff_')
@permission_required('bank.transaction')
def new_transaction_buy_add(request):
    if request.method == 'POST':
        form = NewTransactionBuyForm(request.POST)
        if form.is_valid():
            new_transaction = transaction()
            new_transaction.id = uuid.uuid4()
            new_transaction.date = datetime.datetime.today()
            new_transaction.creator = account.objects.get(last_name='Admin')
            new_transaction.receiver = form.cleaned_data['transaction_receiver']
            new_transaction.sign = '-'
            good_dict = form.clean_goods()[0]
            good_list_id = form.clean_goods()[1]
            goods = shop.objects.filter(id__in=good_list_id).order_by("-cost")
            cnt = 0
            flag = False
            comment = "Чек за покупку: "
            for good in goods:
                cnt += good.cost * good_dict[good]
                comment += f"{good.name}, {good_dict[good]} раз: {good.cost * good_dict[good]}t; "
                if cnt > new_transaction.receiver.balance: flag = True
            if flag: return HttpResponse(f"<h2>На покупку не хватает денег.<br/><br/>{comment}<br/><br/>Есть {new_transaction.receiver.balance}, а надо {cnt}.<a href=\"/\">Назад...</a></h2>")
            new_transaction.cnt = cnt
            new_transaction.history = request.user.account
            new_transaction.comment = comment
            new_transaction.save()
            new_transaction.count()
            return redirect('info-staff')
    else:
        form = NewTransactionBuyForm(initial={})

    return render(request, 'bank/transaction_form_buy.html', {'form': form,})

@permission_required('bank.transaction_base')
def new_transaction_base_add(request):
    if request.method == 'POST':
        form = NewTransactionBaseForm(request.POST)
        if form.is_valid():
            new_transaction = transaction()
            new_transaction.id = uuid.uuid4()
            new_transaction.date = datetime.datetime.today()
            new_transaction.comment = form.cleaned_data['transaction_comment']
            new_transaction.creator = request.user.account
            new_transaction.receiver = form.cleaned_data['transaction_receiver']
            new_transaction.history = request.user.account
            if new_transaction.creator == new_transaction.receiver:
                return HttpResponse("<h2>Неужели вы <em>настолько</em> жадина? <a href=\"/\">Назад...</a></h2>")
            elif account.objects.get(last_name='Admin') == new_transaction.receiver:
                return HttpResponse("<h2>Вы не можете перевести деньги на банковский счёт. Сегодня без донатов. <a href=\"/\">Назад...</a></h2>")
            new_transaction.cnt = form.cleaned_data['transaction_cnt']
            if new_transaction.cnt > request.user.account.balance:
                return HttpResponse("<h2>Вы не можете перевести денег больше, чем у вас есть, хотя вы и гений. <a href=\"/\">Назад...</a>    </h2>")
            new_transaction.save()
            new_transaction.count()
            return redirect('index')
    else:
        transaction_date = datetime.datetime.now()
        transaction_comment = "Не указано"
        transaction_cnt = 0
        form = NewTransactionBaseForm(initial={'transaction_date': transaction_date, 'transaction_comment': transaction_comment, 'transaction_cnt': transaction_cnt})

    return render(request, 'bank/transaction_form.html', {'form': form,})

@permission_required('bank.staff_')
@permission_required('bank.transaction')
def re_new_transaction_add(request, pk):
    transaction_ = get_object_or_404(transaction, pk=pk)
    if request.method == 'POST':
        form = ReNewTransactionStaffForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["delete"]:
                if transaction_.counted: transaction_.uncount()
                transaction_.delete()
            elif form.cleaned_data["edit"]:
                if transaction_.counted: transaction_.uncount()
                else: transaction_.count()
            else:
                transaction_.uncount()
                transaction_.date = form.cleaned_data['transaction_date']
                transaction_.comment = form.cleaned_data['transaction_comment']
                transaction_.sign = form.cleaned_data['transaction_sign']
                transaction_.cnt = form.cleaned_data['transaction_cnt']
                transaction_.history = form.cleaned_data['transaction_history']
                transaction_.save()
                transaction_.count()
            return redirect('info-staff')
    else:
        transaction_history = transaction_.history
        transaction_date = transaction_.date
        transaction_comment = transaction_.comment
        transaction_cnt = transaction_.cnt
        transaction_sign = transaction_.sign
        form = ReNewTransactionStaffForm(initial={'transaction_date': transaction_date, 'transaction_comment': transaction_comment,
               'transaction_cnt': transaction_cnt, 'transaction_sign': transaction_sign, 'transaction_history': transaction_history,})

    return render(request, 'bank/transaction_edit_form.html', {'form': form, 'counted': transaction_.counted,})

@permission_required('bank.staff_')
@permission_required('bank.register')
def new_account_add(request):
    def translit(s: str) -> str:
        ans = ""
        s = s.lower()
        table_d = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'ye', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y',
                   'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', ' ': '_',
                   'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sh', 'ъ': '', 'ы': 'i', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya'}
        for c in s:
            try: ans += table_d[c]
            except KeyError: ans += c
        return ans

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

    if request.method == 'POST':
        form = NewAccountForm(request.POST)
        if form.is_valid():
            new_account = account()

            type_ = form.cleaned_data['type_']
            first_name = form.cleaned_data['first_name']
            middle_name = form.cleaned_data['middle_name']
            last_name = form.cleaned_data['last_name']
            username = f'{translit(first_name[0])}.{translit(middle_name[0])}.{translit(last_name)}'
            for u in User.objects.all():
                if f'{u.username}' == f'{username}': return HttpResponse("<h2>Такой пользователь уже существует. <a href=\"/\">Назад...</a></h2>")
            user_group = form.cleaned_data['user_group']
            party = form.cleaned_data['party']
            len_pass = 8 if type_ == 0 else 12
            password = gen_pass(len_pass)

            if f'{type_}' == '1':
                group_, created = Group.objects.get_or_create(name="pedagogue")
                if created:
                    perms, created = Permission.objects.get_or_create(codename="staff_")
                    group_.permissions.add(perms)
                    perms, created = Permission.objects.get_or_create(codename="transaction")
                    group_.permissions.add(perms)
                    perms, created = Permission.objects.get_or_create(codename="transaction_base")
                    group_.permissions.add(perms)
                    perms, created = Permission.objects.get_or_create(codename="meria")
                    group_.permissions.add(perms)
                    perms, created = Permission.objects.get_or_create(codename="edit_users")
                    group_.permissions.add(perms)
            else: group_, created = Group.objects.get_or_create(name="listener")
            group_.save()
            group_meria, created = Group.objects.get_or_create(name="meria")
            if created:
                perms, created = Permission.objects.get_or_create(codename="staff_")
                group_meria.permissions.add(perms)
                perms, created = Permission.objects.get_or_create(codename="meria")
                group_meria.permissions.add(perms)
            group_meria.save()
            
            new_user = User.objects.create(username=username, password=make_password(password))
            new_user.groups.add(group_)

            new_account.id = uuid.uuid4()
            new_account.user = new_user
            new_account.first_name = first_name
            new_account.middle_name = middle_name
            new_account.last_name = last_name
            new_account.user_group = user_group
            new_account.party = party
            new_account.balance = 0
            new_account.save()

            s_write = f'login: {username}\npassword: {password}\n' + '-' * 30 + '\n'
            f = open("All_users.txt", "a")
            f.write(s_write)
            f.close()

            if form.cleaned_data['save_and_new']:
                return redirect('new-user')
            else:
                return redirect('info-users')
    else:
        type_ = 0
        first_name = "Not stated"
        middle_name = "Not stated"
        last_name = "Not stated"
        user_group = None
        party = 0
        form = NewAccountForm(initial={'type_': type_, 'first_name': first_name, 'middle_name': middle_name, 'last_name': last_name,
                                       'id': id, 'user_group': user_group, 'party': party})
    return render(request, 'bank/account_form.html', {'form': form,})

@permission_required('bank.staff_')
@permission_required('bank.register')
def new_account_full_add(request):
    def translit(s: str) -> str:
        ans = ""
        s = s.lower()
        table_d = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'ye', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y',
                   'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', ' ': '_',
                   'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sh', 'ъ': '', 'ы': 'i', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya'}
        for c in s:
            try: ans += table_d[c]
            except KeyError: ans += c
        return ans

    if request.method == 'POST':
        form = NewAccountFullForm(request.POST)
        if form.is_valid():
            new_account = account()

            type_ = form.cleaned_data['type_']
            first_name = form.cleaned_data['first_name']
            middle_name = form.cleaned_data['middle_name']
            last_name = form.cleaned_data['last_name']
            username = translit(form.cleaned_data['username'])
            for u in User.objects.all():
                if f'{u.username}' == f'{username}': return HttpResponse("<h2>Такой пользователь уже существует. <a href=\"/\">Назад...</a></h2>")
            user_group = form.cleaned_data['user_group']
            party = form.cleaned_data['party']
            password = form.cleaned_data['password']

            if f'{type_}' == '1':
                group_, created = Group.objects.get_or_create(name="pedagogue")
                if created:
                    perms, created = Permission.objects.get_or_create(name="bank.account.staff_")
                    group_.permissions.add(perms)
                    perms, created = Permission.objects.get_or_create(name="bank.account.transaction")
                    group_.permissions.add(perms)
                    perms, created = Permission.objects.get_or_create(name="bank.account.transaction_base")
                    group_.permissions.add(perms)
                    perms, created = Permission.objects.get_or_create(name="bank.account.meria")
                    group_.permissions.add(perms)
                    perms, created = Permission.objects.get_or_create(name="bank.account.edit_users")
                    group_.permissions.add(perms)
            else: group_, created = Group.objects.get_or_create(name="listener")
            group_.save()
            group_meria, created = Group.objects.get_or_create(name="meria")
            if created:
                perms, created = Permission.objects.get_or_create(name="bank.account.staff_")
                group_meria.permissions.add(perms)
                perms, created = Permission.objects.get_or_create(name="bank.account.meria")
                group_meria.permissions.add(perms)
            group_meria.save()
            
            new_user = User.objects.create(username=username, password=make_password(password))
            new_user.groups.add(group_)

            new_account.id = uuid.uuid4()
            new_account.user = new_user
            new_account.first_name = first_name
            new_account.middle_name = middle_name
            new_account.last_name = last_name
            new_account.user_group = user_group
            new_account.party = party
            new_account.balance = 0
            new_account.save()

            s_write = f'login: {username}\npassword: {password}\n' + '-' * 30 + '\n'
            f = open("All_users.txt", "a")
            f.write(s_write)
            f.close()

            if form.cleaned_data['save_and_new']:
                return redirect('new-user')
            else:
                return redirect('info-users')
    else:
        type_ = 0
        first_name = "Not stated"
        middle_name = "Not stated"
        last_name = "Not stated"
        user_group = None
        party = 0
        form = NewAccountFullForm(initial={'type_': type_, 'first_name': first_name, 'middle_name': middle_name, 'last_name': last_name,
                                       'id': id, 'user_group': user_group, 'party': party})
    return render(request, 'bank/account_form.html', {'form': form,})

@permission_required('bank.staff_')
@permission_required('bank.edit_users')
def re_new_account_full_add(request, pk):
    def translit(s: str) -> str:
        ans = ""
        s = s.lower()
        table_d = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'ye', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y',
                   'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', ' ': '_',
                   'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sh', 'ъ': '', 'ы': 'i', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya'}
        for c in s:
            try: ans += table_d[c]
            except KeyError: ans += c
        return ans

    account_ = get_object_or_404(account, id=pk)
    user_ = User.objects.get(id=account_.user.id)
    if request.method == 'POST':
        form = ReNewAccountForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['delete']:
                tr1 = transaction.objects.filter(creator=account_)
                tr2 = transaction.objects.filter(receiver=account_)
                for i in tr1:
                    if i.counted: i.uncount()
                for i in tr2:
                    if i.counted: i.uncount()
                account_.delete()
                user_.delete()
            else:
                first_name = form.cleaned_data['first_name']
                middle_name = form.cleaned_data['middle_name']
                last_name = form.cleaned_data['last_name']
                balance = form.cleaned_data['balance']
                username = translit(form.cleaned_data['username'])
                for u in User.objects.all():
                    if f'{u.username}' == f'{username}': return HttpResponse("<h2>Такой пользователь уже существует. <a href=\"/\">Назад...</a></h2>")
                user_group = form.cleaned_data['user_group']
                party = form.cleaned_data['party']
                
                user_.username = username
                user_.save()

                account_.first_name = first_name
                account_.middle_name = middle_name
                account_.last_name = last_name
                account_.user_group = user_group
                account_.party = party
                account_.balance = balance
                account_.save()
            return redirect('info-users')
    else:
        first_name = account_.first_name
        middle_name = account_.middle_name
        last_name = account_.last_name
        user_group = account_.user_group
        party = account_.party
        balance = account_.balance
        username = user_.username
        form = ReNewAccountForm(initial={'balance': balance, 'first_name': first_name, 'middle_name': middle_name,
               'last_name': last_name, 'user_group': user_group, 'party': party, 'username': username,})
    return render(request, 'bank/form_edit_for_all.html', {'form': form, 'delta': 'аккаунта'})

@login_required
def new_message_add(request):
    if request.method == 'POST':
        form = NewMessageForm(request.POST)
        if form.is_valid():
            new_message = message()
            new_message.id = uuid.uuid4()
            new_message.date = datetime.datetime.today()
            new_message.time = datetime.datetime.now()
            new_message.creator = request.user.account
            new_message.receiver = None
            new_message.text = form.cleaned_data['message_text']
            new_message.anonim = form.cleaned_data['message_anonim']
            #if new_message.creator == new_message.receiver:
            #    return HttpResponse("<h2>Неужели вы <em>настолько</em> одиноки?..<br/>К сожалению, нельзя себе отправлять сообщения.<a href=\"/\">Назад...</a></h2>")
            new_message.save()
            return redirect('messages')
    else:
        form = NewMessageForm(initial={'message_text': '',})

    return render(request, 'bank/messages_new.html', {'form': form,})

@login_required
def new_chat_add(request):
    def make_valid_form(chat_: chat, chat_valid_: chat_valid):
        return f'{chat_valid_.list_members}{chat_.anonim}' if chat_valid_.avaliable else 'None'
    current_user = request.user.account
    if request.method == 'POST':
        form = NewChatForm(request.POST, current_user=current_user)
        if form.is_valid():
            new_message = message()
            new_chat = chat()
            new_chat_valid = chat_valid()

            new_chat.id = uuid.uuid4()
            new_chat.anonim = form.cleaned_data["chat_anonim"]
            new_chat.anonim_legacy = form.cleaned_data["chat_anonim_legacy"]
            new_chat.name = form.cleaned_data["chat_name"]
            new_chat.description = form.cleaned_data["chat_description"]
            members = list(f'{i.id}' for i in form.cleaned_data["chat_members"])
            members.append(f'{request.user.account.id}')
            new_chat.creator = request.user.account
            new_chat.cnt = len(members)
            
            new_message.id = uuid.uuid4()
            new_message.date = datetime.datetime.today()
            new_message.time = datetime.datetime.now()
            new_message.creator = request.user.account
            new_message.receiver = new_chat
            new_message.text = f'Создан чат {new_chat.name} ({new_chat.description}).'
            new_message.anonim = True
            
            new_chat_valid.id = uuid.uuid4()
            new_chat_valid.what_chat = new_chat
            new_chat_valid.avaliable = True
            new_chat_valid.list_members = members
            new_chat_valid.list_messages.append(f'{new_message.id}')
            members = list(form.cleaned_data["chat_members"])
            members.append(request.user.account)

            set_of_chats_valid = list(chat_valid.objects.filter(avaliable=True))

            new_chat.save()
            new_message.save()
            new_chat_valid.save()

            for i in range(len(set_of_chats_valid)):
                if make_valid_form(new_chat, new_chat_valid) == make_valid_form(set_of_chats_valid[i].what_chat, set_of_chats_valid[i]):
                    #return HttpResponse("<h2>Уже сейчас подобный чат существует. Надо только покопаться... не в архиве. <a href=\"/\">Назад...<a/></h2>")
                    return redirect('chats-new-conflict', new_chat.id, new_message.id, new_chat_valid.id, set_of_chats_valid[i].what_chat.id)

            for acc in members: chat_and_acc.objects.create(id = uuid.uuid4(), what_chat = new_chat, what_acc = acc, readen = False)

            return redirect('messages')
    else:
        form = NewChatForm(current_user=current_user)

    return render(request, 'bank/chats_new.html', {'form': form,})

@login_required
def new_chat_add_confilct(request, new_chat_id, new_message_id, new_chat_valid_id, existing_chat_id):
    new_chat = chat.objects.get(id=new_chat_id)
    new_message = message.objects.get(id=new_message_id)
    new_chat_valid = chat_valid.objects.get(id=new_chat_valid_id)
    new_chat_valid.delete()
    new_message.delete()
    new_chat.delete()
    members = account.objects.filter(id__in=list(new_chat_valid.list_members))
    existing_chat = chat.objects.get(id=existing_chat_id)
    if request.method == 'POST':
        form = NewChatFormConflict(request.POST)
        if form.is_valid():
            solve = int(form.cleaned_data['solve'])
            
            if solve == 2:
                return redirect('messages')
            
            if solve == 1:
                existing_chat.archive()
                return redirect('messages')

            if solve == 0:
                new_chat.save()
                new_message.save()
                new_chat_valid.save()
                existing_chat.archive()
                for acc in members: chat_and_acc.objects.create(id = uuid.uuid4(), what_chat = new_chat, what_acc = acc, readen = False)

            return redirect('messages')
    else:
        form = NewChatFormConflict()

    return render(request, 'bank/chats_new_conflict.html', {'form': form,})

@login_required
def chat_view(request, pk):
    chat_ = get_object_or_404(chat, pk=pk)
    chat_valid_ = chat_valid.objects.get(what_chat=chat_)
    chat_and_acc_all_ = chat_valid_.get_all_CAA()
    chat_and_acc_ = chat_and_acc_all_.get(what_acc=request.user.account)
    chat_and_acc_.readen = True
    chat_and_acc_.save()
    message_all_ = chat_valid_.get_all_msg()
    paginator1 = Paginator(message_all_, 20)
    page1 = request.GET.get('page1')
    try:
        items1 = paginator1.page(page1)
    except PageNotAnInteger:
        items1 = paginator1.page(1)
    except EmptyPage:
        items1 = paginator1.page(paginator1.num_pages)
    len_mess = 2000
    if request.method == 'POST':
        form = NewMessageForm_WithoutAnonim(request.POST) if chat_.anonim or not chat_.anonim_legacy else NewMessageForm(request.POST)
        form2 = SetReadStatusForm(request.POST)
        if form.is_valid():
            if len(list(chat_valid_.list_messages)) >= len_mess:
                redirect('messages')
            message_ = message()
            message_.id = uuid.uuid4()
            message_.date = datetime.datetime.today()
            message_.time = datetime.datetime.today()
            message_.creator = request.user.account
            message_.receiver = chat_
            message_.anonim_legacy = chat_.anonim
            message_.text = form.cleaned_data['message_text']
            if chat_.anonim_legacy: message_.anonim = form.cleaned_data['message_anonim']
            else: message_.anonim = chat_.anonim
            message_.save()
            chat_valid_.add_msg(message_)
            if len(list(chat_valid_.list_messages)) >= len_mess:
                last_message = message()
                last_message.id = uuid.uuid4()
                last_message.date = datetime.datetime.today()
                last_message.time = datetime.datetime.today()
                last_message.creator = chat_.creator
                last_message.receiver = chat_
                last_message.anonim_legacy = chat_.anonim
                last_message.text = f'В чате накопилось 2000 сообщений, поэтому он будет заархивирован.\n\nДля вашего удобства будет создан новый подобный чат.'
                last_message.anonim = True
                last_message.save()
                chat_valid_.add_msg(last_message)
                
                new_message = message()
                new_chat = chat()
                new_chat_valid = chat_valid()

                new_chat.id = uuid.uuid4()
                new_chat.anonim = chat_.anonim
                new_chat.anonim_legacy = chat_.anonim_legacy
                new_chat.name = chat_.name
                new_chat.description = chat_.description
                new_chat.creator = chat_.creator
                new_chat.cnt = chat_.cnt
                
                new_message.id = uuid.uuid4()
                new_message.date = datetime.datetime.today()
                new_message.time = datetime.datetime.now()
                new_message.creator = chat_.creator
                new_message.receiver = new_chat
                new_message.text = f'В предыдущем чате был достигнут лимит по количеству сообщений.\n\nВместо него создан аналогичный чат \"{new_chat.name} ({new_chat.description}).\"'
                new_message.anonim = True
                
                new_chat_valid.id = uuid.uuid4()
                new_chat_valid.what_chat = new_chat
                new_chat_valid.avaliable = True
                new_chat_valid.list_members = list(chat_valid_.list_members)
                new_chat_valid.list_messages = []
                new_chat_valid.list_messages.append(f'{new_message.id}')
                members = list(account.objects.filter(id__in=list(chat_valid_.list_members)))

                new_chat.save()
                new_message.save()
                new_chat_valid.save()
                chat_.archive()
                
                for acc in members: chat_and_acc.objects.create(id = uuid.uuid4(), what_chat = new_chat, what_acc = acc, readen = False)

                return redirect(new_chat.get_absolute_url())
            return redirect(chat_.get_absolute_url())
        if form2.is_valid():
            if chat_and_acc_.readen:
                chat_and_acc_.unread_chat()
                return redirect('messages')
            else:
                chat_and_acc_.read_chat()
            return redirect(chat_.get_absolute_url())
    else:
        form2 = SetReadStatusForm()
        anonim = False
        text = ''
        form = NewMessageForm(initial={'message_text': text, 'message_anonim': anonim,}) \
            if not chat_.anonim and chat_.anonim_legacy else NewMessageForm_WithoutAnonim(initial={'message_text': text})

    return render(request, 'bank/chats_view_n.html', {'form': form, 'messages': items1, 'chat': chat_,
                                                      'form2': form2, 'readen_status': chat_and_acc_.readen,})

@login_required
def chat_archived_view(request, pk):
    chat_ = get_object_or_404(chat, pk=pk)
    chat_valid_ = chat_valid.objects.get(what_chat=chat_)
    #chat_and_acc_all_ = chat_valid_.get_all_CAA()
    message_all_ = chat_valid_.get_all_msg()
    paginator1 = Paginator(message_all_, 220)
    page1 = request.GET.get('page1')
    try:
        items1 = paginator1.page(page1)
    except PageNotAnInteger:
        items1 = paginator1.page(1)
    except EmptyPage:
        items1 = paginator1.page(paginator1.num_pages)
    return render(request, 'bank/chats_archived_view_n.html', {'messages': items1, 'chat': chat_,})

@login_required
def chat_archive(request):
    chat_valid_ = chat_valid.objects.exclude(avaliable=True)
    message_all_ = [i.what_chat for i in chat_valid_]
    paginator1 = Paginator(message_all_, 25)
    page1 = request.GET.get('page1')
    try:
        items1 = paginator1.page(page1)
    except PageNotAnInteger:
        items1 = paginator1.page(1)
    except EmptyPage:
        items1 = paginator1.page(paginator1.num_pages)
    return render(request, 'bank/chat_archive.html', {'messages': items1,})

@login_required
def re_new_message_add(request, pk):
    message_ = get_object_or_404(message, pk=pk)
    x = chat_valid.objects.get(what_chat=message_.receiver) if message_.receiver is not None else None
    flag = x is not None
    if not flag: flag = message_.receiver is None
    else: flag = x.avaliable
    if flag:
        if message_.creator == request.user.account:
            anon_prov = message_.anonim and not message_.anonim_legacy

            if request.method == 'POST':
                form = ReNewMessageFormAnonim(request.POST) if anon_prov else ReNewMessageFormBase(request.POST)
                if form.is_valid():
                    if form.cleaned_data['delete']:
                        if message_.receiver is not None:
                            chat_valid_ = chat_valid.objects.get(what_chat=message_.receiver)
                            for i in range(len(chat_valid_.list_messages)):
                                if f'{chat_valid_.list_messages[i]}' == f'{message_.id}':
                                    del chat_valid_.list_messages[i]
                                    break
                        message_.delete()
                    else:
                        message_.text = form.cleaned_data['message_text'] + f"\n\n(Изменено {datetime.date.today()} в {datetime.time(hour=datetime.datetime.now().hour, minute=datetime.datetime.now().minute, second=datetime.datetime.now().second)})"
                        if anon_prov: message_.anonim = form.cleaned_data['message_anonim']
                        message_.save()
                    return redirect('messages-edit')
            else:
                anonim = message_.anonim
                text = f'{message_.text}'
                text = text[:-34] if text[-1] == ')' and "\n\n(Изменено " in text else text
                form = ReNewMessageFormAnonim(initial={'message_text': text, 'message_anonim': anonim,}) \
                    if anon_prov else ReNewMessageFormBase(initial={'message_text': text})

            return render(request, 'bank/messages_edit_n.html', {'form': form,})
        else: return HttpResponse("<h2>Я, конечно, всё понимаю, но <em>этого</em> мне не понять...<br/>К сожалению, вы можете редактировать только свои сообщения. <a href=\"/\">Назад...</a></h2>")
    else: return HttpResponse("<h2>Чат с данным сообщением заархивирован. <a href=\"/\">Назад...<a/></h2>")

@login_required
def re_new_chat_add(request, pk):
    chat_ = get_object_or_404(chat, pk=pk)
    chat_valid_ = chat_valid.objects.get(what_chat=chat_)
    if chat_.creator == request.user.account:
        anon_prov = not chat_.anonim and not chat_.anonim_legacy
        current_users = account.objects.filter(id__in=[uuid.UUID(i) for i in chat_valid_.list_members])
        if request.method == 'POST':
            form = ReNewChatFormAnonim(request.POST, current_users=current_users, current_user=request.user.account)\
                   if anon_prov else ReNewChatFormBase(request.POST, current_users=current_users, current_user=request.user.account)
            if form.is_valid():
                chat_.name = form.cleaned_data['chat_name']
                chat_.description = form.cleaned_data['chat_text']
                if anon_prov: chat_.anonim_legacy = form.cleaned_data['chat_anonim']
                creator_chat = form.cleaned_data['chat_creator']
                if creator_chat is not None: chat_.creator = creator_chat
                chat_.save()
                if form.cleaned_data['delete']:
                    chat_.archive()
                    return redirect('messages')
                return redirect(chat_.get_absolute_url())
        else:
            anonim = chat_.anonim_legacy
            name = chat_.name
            text = chat_.description
            form = ReNewChatFormAnonim(initial={'chat_text': text, 'chat_name': name, 'chat_anonim': anonim,},\
                                       current_users=current_users, current_user=request.user.account) if anon_prov else \
                   ReNewChatFormBase(initial={'chat_text': text, 'chat_name': name,}, current_users=current_users, current_user=request.user.account)

        return render(request, 'bank/chats_edit_n.html', {'form': form,  'chat': chat_,})
    else: return HttpResponse("<h2>Я, конечно, всё понимаю, но <em>этого</em> мне не понять...<br/>К сожалению, вы можете редактировать только те чаты, создателем которых вы являетесь.<a href=\"/\">Назад...</a></h2>")

@permission_required('bank.staff_')
@permission_required('bank.transaction')
def renew_transaction(request):
    return render(request, 'bank/transaction_do.html')

@permission_required('bank.staff_')
@permission_required('bank.transaction')
def undo_transaction(request):
    return render(request, 'bank/transaction_undo.html')

@permission_required('bank.staff_')
@permission_required('bank.register')
def update_all_pass(request):
    return render(request, 'bank/update_all_pass.html')

@permission_required('bank.staff_')
@permission_required('bank.meria')
def new_plan_add(request):
    if request.method == 'POST':
        form = NewPlanAddForm(request.POST)
        if form.is_valid():
            plan_ = plan()
            plan_.id = uuid.uuid4()
            plan_.time = form.cleaned_data['time']
            plan_.comment = form.cleaned_data['comment']
            plan_.number = int(form.cleaned_data['number'])
            plan_.save()
            return redirect('plans')
    else:
        time = ':'.join(f'{datetime.time(hour=datetime.datetime.today().hour, minute=datetime.datetime.today().minute)}'.split(':')[:-1])
        comment = ''
        if plan.objects.all().exists(): number = list(plan.objects.all().order_by('-number'))[-1].number + 1
        else: number = 1
        form = NewPlanAddForm(initial={'number': number, 'comment': comment, 'time': time,})
    return render(request, 'bank/plan_new.html', {'form': form,})

@permission_required('bank.staff_')
@permission_required('bank.meria')
def re_new_plan_add(request, pk):
    plan_ = get_object_or_404(plan, id=pk)
    if request.method == 'POST':
        form = ReNewPlanAddForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['delete']:
                plan_.delete()
            else:
                plan_.time = form.cleaned_data['time']
                plan_.comment = form.cleaned_data['comment']
                plan_.number = int(form.cleaned_data['number'])
                plan_.save()
            return redirect('plans')
    else:
        time = plan_.time
        comment = plan_.comment
        number = plan_.number
        form = ReNewPlanAddForm(initial={'number': number, 'comment': comment, 'time': time,})
    return render(request, 'bank/form_edit_for_all.html', {'form': form, 'delta': 'пункта расписания'})

@permission_required('bank.staff_')
@permission_required('bank.meria')
def new_shop_add(request):
    if request.method == 'POST':
        form = NewShopAddForm(request.POST)
        if form.is_valid():
            shop_ = shop()
            shop_.id = uuid.uuid4()
            shop_.name = form.cleaned_data['name']
            shop_.comment = form.cleaned_data['comment']
            shop_.cost = int(form.cleaned_data['cost'])
            shop_.save()
            return redirect('shop')
    else:
        name = comment = ''
        cost = 0
        form = NewShopAddForm(initial={'cost': cost, 'comment': comment, 'name': name,})
    return render(request, 'bank/shop_new.html', {'form': form,})

@permission_required('bank.staff_')
@permission_required('bank.meria')
def re_new_shop_add(request, pk):
    shop_ = get_object_or_404(shop, id=pk)
    if request.method == 'POST':
        form = ReNewShopAddForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['delete']:
                shop_.delete()
            else:
                shop_.name = form.cleaned_data['name']
                shop_.comment = form.cleaned_data['comment']
                shop_.cost = int(form.cleaned_data['cost'])
                shop_.save()
            return redirect('shop')
    else:
        name = shop_.name
        comment = shop_.comment
        cost = shop_.cost
        form = ReNewShopAddForm(initial={'cost': cost, 'comment': comment, 'name': name,})
    return render(request, 'bank/form_edit_for_all.html', {'form': form, 'delta': 'товара'})

@permission_required('bank.staff_')
@permission_required('bank.meria')
def new_daily_answer_add(request):
    if request.method == 'POST':
        form = NewDailyAnswerAddForm(request.POST)
        if form.is_valid():
            daily_answer_ = daily_answer()
            daily_answer_.id = uuid.uuid4()
            daily_answer_.name = form.cleaned_data['name']
            daily_answer_.text = form.cleaned_data['comment']
            daily_answer_.cnt = int(form.cleaned_data['cost'])
            daily_answer_.status = form.cleaned_data['giga_ans']
            daily_answer_.save()
            return redirect('answers')
    else:
        name = comment = ''
        cost = 0
        giga_ans = False
        form = NewDailyAnswerAddForm(initial={'cost': cost, 'comment': comment, 'name': name, 'giga_ans': giga_ans,})
    return render(request, 'bank/answers_new.html', {'form': form,})

@permission_required('bank.staff_')
@permission_required('bank.meria')
def re_new_daily_answer_add(request, pk):
    daily_answer_ = get_object_or_404(daily_answer, id=pk)
    if request.method == 'POST':
        form = ReNewDailyAnswerAddForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['delete']:
                daily_answer_.delete()
            else:
                daily_answer_.name = form.cleaned_data['name']
                daily_answer_.text = form.cleaned_data['comment']
                daily_answer_.cnt = int(form.cleaned_data['cost'])
                daily_answer_.status = form.cleaned_data['giga_ans']
                daily_answer_.save()
            return redirect('answers')
    else:
        name = daily_answer_.name
        comment = daily_answer_.text
        cost = daily_answer_.cnt
        giga_ans = daily_answer_.status
        form = ReNewDailyAnswerAddForm(initial={'cost': cost, 'comment': comment, 'name': name, 'giga_ans': giga_ans,})
    return render(request, 'bank/form_edit_for_all.html', {'form': form, 'delta': 'задачи'})
