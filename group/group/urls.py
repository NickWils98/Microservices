from django.urls import path

from .views import GroupViewSet

urlpatterns = [
    path('group', GroupViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('group_user', GroupViewSet.as_view({
        'post': 'add_to_group',
    }))
]