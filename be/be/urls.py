"""
URL configuration for be project.

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
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import get_user_data, upload_ssh_key, list_ssh_keys, delete_ssh_key, add_server, list_servers, delete_server

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/user/', get_user_data, name='get_user_data'),
    path('api/ssh-key/upload/', upload_ssh_key, name='upload_ssh_key'),
    path('api/ssh-keys/', list_ssh_keys, name='list_ssh_keys'),
    path('api/ssh-keys/<int:pk>/delete/', delete_ssh_key, name='delete_ssh_key'),
    path('api/servers/add/', add_server, name='add_server'),
    path('api/servers/', list_servers, name='list_servers'),
    path('api/servers/<int:pk>/delete/', delete_server, name='delete_server'),
]
