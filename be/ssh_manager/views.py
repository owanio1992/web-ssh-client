from rest_framework import viewsets
from .models import SSHKey, Server
from .serializers import SSHKeySerializer, ServerSerializer

class SSHKeyViewSet(viewsets.ModelViewSet):
    queryset = SSHKey.objects.all()
    serializer_class = SSHKeySerializer

class ServerViewSet(viewsets.ModelViewSet):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer
