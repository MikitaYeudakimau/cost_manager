from django.urls import path
from rest_framework.routers import DefaultRouter

from manager import views

router = DefaultRouter()
router.register('category',views.CategoryViewSet)
router.register('account',views.AccountViewSet)
router.register('transaction',views.TransactionViewSet)
urlpatterns = [

]

urlpatterns += router.urls
