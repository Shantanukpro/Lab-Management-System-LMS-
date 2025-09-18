from rest_framework.routers import DefaultRouter
from .views import LabViewSet, PCViewSet

router = DefaultRouter()
router.register(r'labs', LabViewSet, basename='lab')
router.register(r'pcs', PCViewSet, basename='pc')

urlpatterns = router.urls
