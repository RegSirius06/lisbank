from django.urls import re_path
from bank import views
#from django.conf.urls import url

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    #re_path(r'^book/(?P<pk>[-\w]+)$', views.BookDetailView.as_view(), name='book-detail'),
    re_path(r'^rules/$', views.rules, name='rules'),
    #re_path(r'^author/(?P<pk>[-\w]+)$', views.AuthorDetailView.as_view(), name='author-detail'),
    re_path(r'^shop/$', views.shop_view, name='shop'),
    re_path(r'^info_staff/$', views.info_for_staff, name='info-staff'),
    re_path(r'^all_balances/$', views.TransactionsListView.as_view(), name='accounts'),
    re_path(r'^transactions/(?P<pk>[-\w]+)$', views.TransactionsDetailView.as_view(), name='account-detail'),
    re_path(r'^my_transactions/$', views.MyTransactionsView.as_view(), name='my-transactions'),
    #re_path(r'^transactions/(?P<pk>[-\w]+)/new/$', views.new_transaction_add, name='new-transaction'),
    #re_path(r'^transactions/create/$', views.NewTransactionBaseCreate.as_view(), name='new-transaction'),
    re_path(r'^transactions/create/$', views.new_transaction_base_add, name='new-transaction-base'),
    re_path(r'^transactions_/create/$', views.new_transaction_staff_add, name='new-transaction-staff'),
]