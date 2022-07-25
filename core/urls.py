from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'category', views.CategoryModelViewSet)
router.register(r'transaction', views.TransactionModelViewSet, basename='transaction')
# router.register(r'report', views.TransactionReportApiView.as_view(),basename='report')
# urlpatterns = router.urls
urlpatterns = [
    path('report/', views.TransactionReportApiView.as_view(), name="report"),
    path('', include(router.urls)),
]
