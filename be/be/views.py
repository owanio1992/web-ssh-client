from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User
from .models import SSHKey

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
