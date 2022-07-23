from rest_framework import routers
from . import views

router = routers.SimpleRouter()
router.register(r'category', views.CategoryModelViewSet)
router.register(r'transaction', views.TransactionModelViewSet)
urlpatterns = router.urls
