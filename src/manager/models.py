from django.db import models
from django.contrib.auth.models import User

#TODO: description in transact model can be blank
class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)
    added_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name="category_add_user")

    def __str__(self):
        return f"Category '{self.name}'"


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="account_user",unique=True)
    balance = models.DecimalField(max_digits=10,decimal_places=2)
    category = models.ManyToManyField(Category, related_name="account_category")

    def __str__(self):
        return f"Account {self.user}"


class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="transaction_account")
    sum = models.DecimalField(max_digits=10,decimal_places=2)
    time = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="transaction_category")
    organization = models.CharField(max_length=45)
    description = models.TextField()
