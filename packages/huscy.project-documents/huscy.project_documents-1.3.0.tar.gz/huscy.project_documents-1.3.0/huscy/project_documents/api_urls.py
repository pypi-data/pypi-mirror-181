from rest_framework.routers import DefaultRouter

from huscy.project_documents import views
from huscy.projects.urls import project_router


router = DefaultRouter()
router.register('documenttypes', views.DocumentTypeViewSet)

project_router.register('documents', views.DocumentViewSet, basename='document')

urlpatterns = router.urls
urlpatterns += project_router.urls
