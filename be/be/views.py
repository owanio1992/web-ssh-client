from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User
from .models import SSHKey, Server, Role, UserRole

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

    # Check for uniqueness within the same site
    if Server.objects.filter(site_name=site_name, server_name=server_name).exists():
        return Response({'error': f'Server name "{server_name}" already exists in site "{site_name}".'}, status=status.HTTP_400_BAD_REQUEST)

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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_roles(request):
    roles = Role.objects.all()
    data = [{'id': role.id, 'name': role.name} for role in roles]
    return Response(data)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_role(request):
    name = request.data.get('name')
    if not name:
        return Response({'error': 'Name is required.'}, status=status.HTTP_400_BAD_REQUEST)
    role = Role(name=name)
    role.save()
    return Response({'message': 'Role created successfully.'}, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_role(request, pk):
    try:
        role = Role.objects.get(pk=pk)
    except Role.DoesNotExist:
        return Response({'error': 'Role not found.'}, status=status.HTTP_404_NOT_FOUND)

    # Delete any UserRole entries that reference this role
    UserRole.objects.filter(role=role).delete()

    role.delete()
    return Response({'message': 'Role deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_permissions(request):
    permissions = Permission.objects.all()
    data = [{'id': p.id, 'role_id': p.role.id, 'server_ids': [server.id for server in p.servers.all()]} for p in permissions]
    return Response(data)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def add_permission(request):
    role_id = request.data.get('role_id')
    server_ids = request.data.get('server_ids')

    if not role_id or not server_ids:
        return Response({'error': 'Role ID and Server IDs are required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        role = Role.objects.get(pk=role_id)
        servers = Server.objects.filter(pk__in=server_ids)
    except Role.DoesNotExist:
        return Response({'error': 'Role not found.'}, status=status.HTTP_400_BAD_REQUEST)
    except Server.DoesNotExist:
        return Response({'error': 'One or more servers not found.'}, status=status.HTTP_400_BAD_REQUEST)

    permission = Permission(role=role)
    permission.save()
    permission.servers.set(servers)

    return Response({'message': 'Permission added successfully.'}, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_permission(request, pk):
    try:
        permission = Permission.objects.get(pk=pk)
    except Permission.DoesNotExist:
        return Response({'error': 'Permission not found.'}, status=status.HTTP_404_NOT_FOUND)

    permission.delete()
    return Response({'message': 'Permission deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_user_roles(request):
    user_roles = UserRole.objects.all()
    data = [{'id': ur.id, 'user_id': ur.user.id, 'role_id': ur.role.id} for ur in user_roles]
    return Response(data)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def add_user_to_role(request):
    user_id = request.data.get('user_id')
    role_id = request.data.get('role_id')

    if not user_id or not role_id:
        return Response({'error': 'User ID and Role ID are required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(pk=user_id)
        role = Role.objects.get(pk=role_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found.'}, status=status.HTTP_400_BAD_REQUEST)
    except Role.DoesNotExist:
        return Response({'error': 'Role not found.'}, status=status.HTTP_400_BAD_REQUEST)

    user_role = UserRole(user=user, role=role)
    user_role.save()

    return Response({'message': 'User added to role successfully.'}, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def remove_user_from_role(request, pk):
    try:
        user_role = UserRole.objects.get(pk=pk)
    except UserRole.DoesNotExist:
        return Response({'error': 'User role not found.'}, status=status.HTTP_404_NOT_FOUND)

    user_role.delete()
    return Response({'message': 'User removed from role successfully.'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_users(request):
    users = User.objects.all()
    data = [{'id': user.id, 'username': user.username} for user in users]
    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_permissions(request):
    permissions = Permission.objects.all()
    data = [{'id': p.id, 'role_id': p.role.id, 'site_name': p.site_name, 'server_name': p.server_name} for p in permissions]
    return Response(data)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def add_permission(request):
    role_id = request.data.get('role_id')
    site_name = request.data.get('site_name')
    server_name = request.data.get('server_name')

    if not role_id or not site_name or not server_name:
        return Response({'error': 'All fields are required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        role = Role.objects.get(pk=role_id)
    except Role.DoesNotExist:
        return Response({'error': 'Role not found.'}, status=status.HTTP_400_BAD_REQUEST)

    permission = Permission(role=role, site_name=site_name, server_name=server_name)
    permission.save()

    return Response({'message': 'Permission added successfully.'}, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_permission(request, pk):
    try:
        permission = Permission.objects.get(pk=pk)
    except Permission.DoesNotExist:
        return Response({'error': 'Permission not found.'}, status=status.HTTP_404_NOT_FOUND)

    permission.delete()
    return Response({'message': 'Permission deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
