from rest_framework.routers import DefaultRouter
from .views import GameViewSet


router = DefaultRouter()
router.register(r'', GameViewSet, basename='games')
urlpatterns = router.urls

