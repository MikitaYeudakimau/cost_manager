from django.contrib import admin
from manager.models import Account, Category, Transaction

admin.site.register(Account)
admin.site.register(Transaction)
admin.site.register(Category)
