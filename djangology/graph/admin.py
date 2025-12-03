from django.contrib import admin

from graph.models import Account, Transaction, Entity


class AccountAdmin(admin.ModelAdmin):
    save_as = True


class TransactionAdmin(admin.ModelAdmin):
    save_as = True


class EntityAdmin(admin.ModelAdmin):
    save_as = True


admin.site.register(Account, AccountAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Entity, EntityAdmin)
