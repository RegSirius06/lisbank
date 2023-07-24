from django.contrib import admin
from bank.models import account, transaction, rools, shop, plan, message, daily_answer, chat, chat_and_acc, chat_valid

@admin.register(chat)
class ChatAdmin(admin.ModelAdmin):
    pass

@admin.register(chat_valid)
class ChatValidAdmin(admin.ModelAdmin):
    pass

@admin.register(chat_and_acc)
class ChatAndAccAdmin(admin.ModelAdmin):
    pass

@admin.register(account)
class AccountAdmin(admin.ModelAdmin):
    list_filter = ["user_group", "party"]
    pass

@admin.register(message)
class MessageAdmin(admin.ModelAdmin):
    list_filter = ["date", "receiver", "creator"]
    pass

@admin.register(daily_answer)
class AnswerAdmin(admin.ModelAdmin):
    pass

@admin.register(plan)
class PlanAdmin(admin.ModelAdmin):
    pass

@admin.register(transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_filter = ["date", "receiver", "creator", "history", "counted"]
    pass

@admin.register(shop)
class ShopAdmin(admin.ModelAdmin):
    pass

@admin.register(rools)
class Rools_Admin(admin.ModelAdmin):
    pass