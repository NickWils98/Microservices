from django.urls import path

from .views import MovieViewSet

urlpatterns = [
    path('movielist', MovieViewSet.as_view({
        'get': 'list'
    }))
]