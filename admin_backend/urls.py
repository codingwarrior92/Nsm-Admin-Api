"""
URL configuration for admin_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from authentication.authentication import SwaggerTokenAuthentication

schema_view = get_schema_view(
   openapi.Info(
      title="Admin-API",
      default_version='v1',
      description="This is Admin API Doc.",
      contact=openapi.Contact(email="dream.dev1992@gmail.com"),
      license=openapi.License(name="RAS Dev Group"),
   ), 
   public=True,
   permission_classes=(permissions.AllowAny,),
   authentication_classes=(SwaggerTokenAuthentication, )
)
urlpatterns = [
    path('auth/', include('authentication.urls')),
    path('coin/', include('coinmarketcap.urls')),
    path('client/', include('client.urls')),
    path('keyword/', include('keywords.urls')),

    path('swagger(<format>.json|.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
