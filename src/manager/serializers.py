from django.db.models import Q
from rest_framework import serializers

from manager import models


class CategorySerializer(serializers.ModelSerializer):
    added_by = serializers.StringRelatedField()

    class Meta:
        model = models.Category
        fields = ['id', 'name', 'added_by']


class AccountCategoryField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        return models.Category.objects.filter(
            Q(added_by__username="admin") | Q(added_by=self.context['request'].user.id))

    def to_representation(self, value):
        return f"{value.name}"

    def to_internal_value(self, data):
        return models.Category.objects.get(name=data)


class AccountSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    balance = serializers.StringRelatedField()
    category = AccountCategoryField(many=True)
    transaction_account = serializers.StringRelatedField(many=True,read_only=True)

    class Meta:
        model = models.Account
        fields = ['id', 'user', 'balance', 'category','transaction_account']


class TransactionCategoryField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        return models.Category.objects.filter(
            Q(added_by__username="admin") | Q(added_by=self.context['request'].user.id))

    def to_representation(self, value):
        return f"{models.Category.objects.get(pk=value.pk).name}"

    def to_internal_value(self, data):
        return models.Category.objects.get(name=data)


class TransactionSerializer(serializers.ModelSerializer):
    account = serializers.StringRelatedField()
    category = TransactionCategoryField()

    class Meta:
        model = models.Transaction
        fields = ['id', 'account', 'sum', 'time', 'category', 'organization', 'description']
