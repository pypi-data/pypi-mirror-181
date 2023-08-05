import warnings

from rest_framework.routers import DefaultRouter

from huscy.project_documents import views
from huscy.projects.urls import project_router


warnings.warn(
    'This module is deprecated and might be removed in a future version. '
    'Please use `api_urls.py` instead.',
    DeprecationWarning
)


router = DefaultRouter()
router.register('documenttypes', views.DocumentTypeViewSet)

project_router.register('documents', views.DocumentViewSet, basename='document')

urlpatterns = router.urls
urlpatterns += project_router.urls
