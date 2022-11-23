from django.db.models import Q
from rest_framework import viewsets, status, mixins, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from djoser.views import UserViewSet
from manager import models, serializers


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

    def get_queryset(self):
        if self.request.user.is_staff is True:
            return models.Transaction.objects.all()
        else:
            return models.Transaction.objects.filter(account__user=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            super().create(request, *args, **kwargs)
        except:
            return Response('Please, make sure, that your account is registered', status=status.HTTP_404_NOT_FOUND)
