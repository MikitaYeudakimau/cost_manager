from django.urls import path
from rest_framework.routers import DefaultRouter

from manager import views

router = DefaultRouter()
router.register('category',views.CategoryViewSet,basename="category")
router.register('account',views.AccountViewSet,basename="account")
router.register('transaction',views.TransactionViewSet,basename="transaction")
urlpatterns = [

]

urlpatterns += router.urls
