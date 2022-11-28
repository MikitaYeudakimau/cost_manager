from decimal import Decimal

from django.db.models import Q
from manager import models, serializers
from manager.signals import signals
from rest_framework import filters, mixins, status, viewsets
from rest_framework.response import Response


class CategoryViewSet(viewsets.ModelViewSet):
    # queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer

    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user)

    def get_queryset(self):
        if self.request.user.is_staff is True:
            return models.Category.objects.all()
        else:
            return models.Category.objects.filter(Q(added_by=self.request.user) | Q(added_by__is_staff=True))

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.added_by.is_staff is True:
            return Response("You cannot delete basic categories", status=status.HTTP_403_FORBIDDEN)
        else:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_200_OK)


class AccountViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    serializer_class = serializers.AccountSerializer

    def get_queryset(self):
        if self.request.user.is_staff is True:
            return models.Account.objects.all()
        else:
            return models.Account.objects.filter(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if self.request.user.is_staff is True:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response("You have no rights for this action. Ask support manager",
                            status=status.HTTP_403_FORBIDDEN)


class TransactionViewSet(mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin,
                         viewsets.GenericViewSet):
    serializer_class = serializers.TransactionSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['sum', 'date']

    def get_queryset(self):
        if self.request.user.is_staff is True:
            return models.Transaction.objects.all()
        else:
            return models.Transaction.objects.filter(account__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(account=models.Account.objects.get(user=self.request.user))
        account_name = self.request.user.username
        amount = Decimal(serializer.data['sum'])
        signals.balance_change.send(sender=self.__class__, account_name=account_name, amount=amount)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        account = self.request.user
        if models.Account.objects.filter(user__username=account).exists() is False:
            return Response("Please, make sure your account is active", status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
