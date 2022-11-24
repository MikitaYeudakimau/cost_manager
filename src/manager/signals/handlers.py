from django.db.models.signals import post_save
from django.dispatch import receiver
from djoser.signals import user_registered
from manager import models
from .signals import balance_change


@receiver(user_registered)
def auto_create_account(sender, user, request,**kwargs):
    """
    For adding only through djoser
    """
    instance = models.Account.objects.create(user=user, balance=0)
    for i in models.Category.objects.filter(added_by__username="admin"):
        instance.category.add(i)


# @receiver(post_save,sender=models.User)
# def auto_create_account_through_admin_panel(sender,instance,created,**kwargs):
#     """
#      For adding through admin panel and djoser
#     """
#     if created:
#         instance = models.Account.objects.create(user=instance, balance=0)
#         for i in models.Category.objects.filter(added_by__username="admin"):
#             instance.category.add(i)


@receiver(balance_change)
def balance_changing(sender, account_name,amount,**kwargs):
    """
    For changing account's balance after transaction's completion
    """
    # print(data)
    obj = models.Account.objects.get(user__username=account_name)
    obj.balance -=amount
    obj.save()
