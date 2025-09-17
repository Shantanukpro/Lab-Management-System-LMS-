from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LabViewSet, PCViewSet

router = DefaultRouter()
router.register(r'labs', LabViewSet)
router.register(r'pcs', PCViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
