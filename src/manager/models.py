from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return f"Category '{self.name}'"


class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="account_user")
    balance = models.DecimalField(max_digits=10,decimal_places=2)
    category = models.ManyToManyField(Category, related_name="account_category")

    def __str__(self):
        return f"{self.user}'s account"

#TODO creation user-> auto create=ion of account and make balance
#TODO adter transact change balance auto
#TODO add new categories through account model
# TODO add to category model field user ( to filter categories for each one)
class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="transaction_account")
    sum = models.DecimalField(max_digits=10,decimal_places=2)
    time = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="transaction_category")
    organization = models.CharField(max_length=45)
    description = models.TextField()
