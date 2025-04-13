from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItemViewSet, PurchaseHeaderViewSet, SellHeaderViewSet, PurchaseDetailListCreate, SellDetailListCreate, ReportView

router = DefaultRouter()
router.register(r'items', ItemViewSet, basename='item')
router.register(r'purchase', PurchaseHeaderViewSet, basename='purchase')
router.register(r'sell', SellHeaderViewSet, basename='sell')

urlpatterns = [
    path('', include(router.urls)),
    path('purchase/<str:header_code>/details/', PurchaseDetailListCreate.as_view(), name='purchase-details'),
    path('sell/<str:header_code>/details/', SellDetailListCreate.as_view(), name='sell-details'),
    path('report/<str:item_code>/', ReportView.as_view(), name='report'),
]