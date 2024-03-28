from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from first_lab.views import *

schema_view = get_schema_view(
    openapi.Info(
        title="Swagger",
        default_version='v1',
        description="Your API description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@yourapi.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

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
    path('booklovers/<int:pk>/', BookLoverViewSetById.as_view(
        {'get': 'get',
         'put': 'update',
         'delete': 'delete'}
    ), name='book-lovers-details'),
    path('booklovers/', BookLoverViewSet.as_view(
        {'get': 'get'}
    ), name='book-lovers'),
    path('auth/login/', AuthViewSet.as_view({'post': 'login'}), name='login'),
    path('auth/register/', AuthViewSet.as_view({'post': 'register'}), name='register'),
    path('auth/changepassword/', AuthViewSet.as_view({'post': 'change_password'}), name='change_password'),
    path('auth/logout/', AuthViewSet.as_view({'post': 'logout'}), name='logout'),
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
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
