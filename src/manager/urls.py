from manager import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('category', views.CategoryViewSet, basename="category")
router.register('account', views.AccountViewSet, basename="account")
router.register('transaction', views.TransactionViewSet, basename="transaction")
urlpatterns = [

]

urlpatterns += router.urls
