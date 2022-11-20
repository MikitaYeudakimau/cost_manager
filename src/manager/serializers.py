from rest_framework import serializers

from manager import models


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = "__all__"


class AccountSerializer(serializers.ModelSerializer):
    # category = PrimaryKeyRelatedField(allow_empty=False, many=True, queryset=Category.objects.all())
    class Meta:
        model = models.Account
        fields = ['id', 'user', 'balance', 'category']


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Transaction
        fields = "__all__"
