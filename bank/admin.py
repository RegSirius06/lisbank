from django.contrib import admin
from bank.models import account, transaction, rule_u, rule_a, rule_t, rule_p, shop

@admin.register(account)
class AccountAdmin(admin.ModelAdmin):
    pass

@admin.register(transaction)
class TransactionAdmin(admin.ModelAdmin):
    pass

@admin.register(shop)
class ShopAdmin(admin.ModelAdmin):
    pass

@admin.register(rule_u)
class Rool_U_Admin(admin.ModelAdmin):
    pass

@admin.register(rule_a)
class Rool_A_Admin(admin.ModelAdmin):
    pass

@admin.register(rule_t)
class Rool_T_Admin(admin.ModelAdmin):
    pass

@admin.register(rule_p)
class Rool_P_Admin(admin.ModelAdmin):
    pass