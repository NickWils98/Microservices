from django.urls import path

from .views import UserViewSet

urlpatterns = [
    path('register', UserViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('login', UserViewSet.as_view({
        'get': 'retrieve',
    })),
    path('user_exists', UserViewSet.as_view({
        'get': 'exists',
    }))
]