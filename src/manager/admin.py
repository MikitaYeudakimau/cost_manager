from django.contrib import admin

from manager.models import Account, Transaction, Category
admin.site.register(Account)
admin.site.register(Transaction)
admin.site.register(Category)