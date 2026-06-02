from django.urls import path
from .views import links_page

urlpatterns = [
    path('', links_page, name='links_page'),
]
