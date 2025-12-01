from django.contrib import admin

from graph.models import Account, Transaction, Entity


class NodeAdmin(admin.ModelAdmin):
    save_as = True


class EdgeAdmin(admin.ModelAdmin):
    save_as = True


class GraphAdmin(admin.ModelAdmin):
    save_as = True


admin.site.register(Account, NodeAdmin)
admin.site.register(Transaction, EdgeAdmin)
admin.site.register(Entity, GraphAdmin)
