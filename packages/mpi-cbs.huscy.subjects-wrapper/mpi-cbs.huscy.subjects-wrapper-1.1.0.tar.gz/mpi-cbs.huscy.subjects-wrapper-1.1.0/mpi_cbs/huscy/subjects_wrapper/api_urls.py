from rest_framework.routers import DefaultRouter

from .views import WrappedSubjectViewSet


router = DefaultRouter()
router.register('wrappedsubjects', WrappedSubjectViewSet)


urlpatterns = router.urls
