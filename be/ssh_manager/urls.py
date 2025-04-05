from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'sshkeys', views.SSHKeyViewSet)
router.register(r'servers', views.ServerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
