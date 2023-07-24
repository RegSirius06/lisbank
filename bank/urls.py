from django.urls import re_path
from bank import views
#from django.conf.urls import url

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^rules/$', views.rools_view, name='rules'),

    re_path(r'^shop/$', views.shop_view, name='shop'),
    re_path(r'^shop/new/$', views.new_shop_add, name='shop-new'),
    re_path(r'^shop/edit/(?P<pk>[-\w]+)$', views.re_new_shop_add, name='shop-renew'),

    re_path(r'^plan/$', views.plan_x, name='plans'),
    re_path(r'^plan/new/$', views.new_plan_add, name='plans-new'),
    re_path(r'^plan/edit/(?P<pk>[-\w]+)$', views.re_new_plan_add, name='plans-renew'),

    re_path(r'^daily_answers/$', views.answers, name='answers'),
    re_path(r'^daily_answers/new/$', views.new_daily_answer_add, name='answers-new'),
    re_path(r'^daily_answers/edit/(?P<pk>[-\w]+)$', views.re_new_daily_answer_add, name='answers-renew'),

    re_path(r'^messages/$', views.home, name='messages'),
    re_path(r'^messages/new/$', views.new_message_add, name='messages-new'),
    re_path(r'^messages/edit/$', views.home_send, name='messages-edit'),
    re_path(r'^messages/edit/(?P<pk>[-\w]+)/$', views.re_new_message_add, name='messages-edit-n'),

    re_path(r'^chats/new/$', views.new_chat_add, name='chats-new'),
    re_path(r'^chats/new/conflict/(?P<new_chat_id>[-\w]+)/(?P<new_message_id>[-\w]+)/(?P<new_chat_valid_id>[-\w]+)/(?P<existing_chat_id>[-\w]+)/$',
            views.new_chat_add_confilct, name='chats-new-conflict'),
    re_path(r'^chats/archive/$', views.chat_archive, name='chats-archived'),
    re_path(r'^chats/archive/(?P<pk>[-\w]+)/$', views.chat_archived_view, name='chats-archived-n'),
    re_path(r'^chats/(?P<pk>[-\w]+)/$', views.chat_view, name='chats-n'),
    re_path(r'^chats/(?P<pk>[-\w]+)/edit/$', views.re_new_chat_add, name='chats-edit-n'),

    re_path(r'^all_balances/$', views.TransactionsListView.as_view(), name='accounts'),
    re_path(r'^my_transactions/$', views.MyTransactionsView.as_view(), name='my-transactions'),

    re_path(r'^transactions/info/$', views.AllTransactionsListView.as_view(), name='info-staff'),
    re_path(r'^transactions/delete/$', views.undo_transaction, name='undo'),
    re_path(r'^transactions/update/$', views.renew_transaction, name='do'),
    re_path(r'^transactions/edit/(?P<pk>[-\w]+)/$', views.re_new_transaction_add, name='transaction-edit'),
    
    re_path(r'^transactions/create/$', views.new_transaction_base_add, name='new-transaction-base'),
    re_path(r'^transactions/create/staff/$', views.new_transaction_staff_add, name='new-transaction-staff'),
    re_path(r'^transactions/create/full/$', views.new_transaction_full_add, name='new-transaction-full'),
    re_path(r'^transactions/create/buy/$', views.new_transaction_buy_add, name='new-transaction-buy'),
    re_path(r'^transactions/create/party/$', views.new_transaction_staff_party_add, name='new-transaction-party'),
    re_path(r'^transactions/(?P<pk>[-\w]+)/$', views.TransactionsDetailView.as_view(), name='account-detail'),
    
    re_path(r'^account/info/$', views.account_info, name='info-users'),
    re_path(r'^account/create/$', views.new_account_add, name='new-user'),
    re_path(r'^account/create/custom/$', views.new_account_full_add, name='new-user-custom'),
    re_path(r'^account/edit/all_pass/$', views.update_all_pass, name='update-all-pass'),
    re_path(r'^account/edit/(?P<pk>[-\w]+)/$', views.re_new_account_full_add, name='account-edit-n'),
]