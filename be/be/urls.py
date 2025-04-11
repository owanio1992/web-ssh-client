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
# Added get_user_roles, update_user_roles
from .views import (
    get_user_data, upload_ssh_key, list_ssh_keys, delete_ssh_key,
    add_server, list_servers, delete_server,
    list_roles, create_role, delete_role, get_role, update_permissions,
    list_user_roles, add_user_to_role, remove_user_from_role,
    list_users, get_user_roles, update_user_roles
)

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
    path('api/roles/', list_roles, name='list_roles'),
    path('api/roles/create/', create_role, name='create_role'),
    path('api/roles/<int:pk>/delete/', delete_role, name='delete_role'),
    path('api/user-roles/', list_user_roles, name='list_user_roles'),
    path('api/user-roles/add/', add_user_to_role, name='add_user_to_role'),
    path('api/user-roles/<int:pk>/delete/', remove_user_from_role, name='remove_user_from_role'),
    path('api/users/', list_users, name='list_users'),
    path('api/roles/<int:pk>/', get_role, name='get_role'),
    path('api/roles/<int:pk>/update_permissions/', update_permissions, name='update_permissions'),
    # New URLs for user-specific roles
    path('api/users/<int:user_id>/roles/', get_user_roles, name='get_user_roles'),
    path('api/users/<int:user_id>/update_roles/', update_user_roles, name='update_user_roles'),
]
