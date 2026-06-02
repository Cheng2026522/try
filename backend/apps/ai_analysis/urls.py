from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AIAnalysisResultViewSet, AnalysisHistoryViewSet

router = DefaultRouter()
router.register('results', AIAnalysisResultViewSet)
router.register('history', AnalysisHistoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
