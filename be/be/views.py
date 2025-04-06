from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User
from .models import SSHKey, Server

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_data(request):
    user = request.user
    groups = [{'id': group.id, 'name': group.name} for group in user.groups.all()]
    return Response({
        'first_name': user.first_name,
        'last_name': user.last_name,
        'last_login': user.last_login,
        'groups': groups
    })

@api_view(['POST'])
@permission_classes([IsAdminUser]) # For now, just require admin user
def upload_ssh_key(request):
    name = request.data.get('name')
    key_content = request.data.get('key_content')

    if not name or not key_content:
        return Response({'error': 'Name and key content are required.'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if an SSH key with the same name already exists
    if SSHKey.objects.filter(name=name).exists():
        return Response({'error': 'SSH key with this name already exists.'}, status=status.HTTP_400_BAD_REQUEST)

    ssh_key = SSHKey(name=name, key_content=key_content)
    ssh_key.save()

    return Response({'message': 'SSH key uploaded successfully.'}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_ssh_keys(request):
    ssh_keys = SSHKey.objects.all()
    data = [{'id': key.id, 'name': key.name, 'key': key.key_content} for key in ssh_keys]
    return Response(data)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_ssh_key(request, pk):
    try:
        ssh_key = SSHKey.objects.get(pk=pk)
    except SSHKey.DoesNotExist:
        return Response({'error': 'SSH key not found.'}, status=status.HTTP_404_NOT_FOUND)

    ssh_key.delete()
    return Response({'message': 'SSH key deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def add_server(request):
    site_name = request.data.get('site_name')
    server_name = request.data.get('server_name')
    user = request.data.get('user')
    host = request.data.get('host')
    ssh_key_id = request.data.get('ssh_key')

    if not site_name or not server_name or not user or not host or not ssh_key_id:
        return Response({'error': 'All fields are required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        ssh_key = SSHKey.objects.get(pk=ssh_key_id)
    except SSHKey.DoesNotExist:
        return Response({'error': 'SSH key not found.'}, status=status.HTTP_400_BAD_REQUEST)

    server = Server(site_name=site_name, server_name=server_name, user=user, host=host, ssh_key=ssh_key)
    server.save()

    return Response({'message': 'Server added successfully.'}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_servers(request):
    servers = Server.objects.all()
    data = [{'id': server.id, 'site_name': server.site_name, 'server_name': server.server_name, 'user': server.user, 'host': server.host, 'ssh_key_name': server.ssh_key.name} for server in servers]
    return Response(data)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_server(request, pk):
    try:
        server = Server.objects.get(pk=pk)
    except Server.DoesNotExist:
        return Response({'error': 'Server not found.'}, status=status.HTTP_404_NOT_FOUND)

    server.delete()
    return Response({'message': 'Server deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
