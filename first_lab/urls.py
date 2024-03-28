from django.urls import path

from first_lab.views import *

urlpatterns = [
    path('regions/<int:pk>/', RegionViewSetById.as_view(
        {'get': 'get',
         'put': 'update',
         'delete': 'delete'}
    ), name='region-detail'),
    path('regions/', RegionViewSet.as_view({
        'get': 'get',
        'post': 'post'}
    ), name='regions'),
    path('booklover/<int:id>', BookLoverViewSetById.as_view(
        {'get': 'get',
         'put': 'update',
         'delete': 'delete'}
    ), name='book-lovers-details'),
    path('auth/login/', AuthViewSet.as_view({'post': 'login'}), name='login'),
    path('publishers/', PublisherViewSet.as_view(
        {'get': 'list',
         'post': 'create'}
    ), name='publisher-list'),
    path('publishers/<int:pk>/', PublisherViewSet.as_view(
        {'get': 'retrieve',
         'put': 'update',
         'delete': 'destroy'}
    ), name='publisher-detail'),
    path('books/', BookViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='book-list'),
    path('books/<int:pk>/', BookViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    }), name='book-detail'),
]
