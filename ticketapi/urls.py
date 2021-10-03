"""ticketapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from rest_framework.schemas import get_schema_view
from rest_framework.routers import DefaultRouter
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
import debug_toolbar
import ticketapi.api.views as views


public_router = DefaultRouter()
public_router.register(r'events', views.EventViewSet)
public_router.register(r'events', views.EventDetailsViewSet)

urlpatterns = [
    path('', views.root, name='root'),
    path('admin/', admin.site.urls),
    path('api/', include(public_router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('openapi/', get_schema_view(
        title="Ticket API",
        description="API for making reservations for events",
        version="1.0.0",
        public=True,
    ), name='openapi-schema'),
    path('docs/', TemplateView.as_view(
        template_name='api/swagger-ui.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='swagger-ui'),
    path('__debug__/', include(debug_toolbar.urls)),
]
