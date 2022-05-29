from django.urls import path

from .views import FriendViewSet

urlpatterns = [
    path('friend', FriendViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('friend_exists', FriendViewSet.as_view({
        'get': 'exists',
    }))
]