from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FileCategoryViewSet, UploadedFileViewSet, FileDownloadView

router = DefaultRouter()
router.register('categories', FileCategoryViewSet)
router.register('files', UploadedFileViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('download/<int:pk>/', FileDownloadView.as_view({'get': 'retrieve'}), name='file_download'),
]
