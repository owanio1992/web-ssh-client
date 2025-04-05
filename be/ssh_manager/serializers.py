from rest_framework import serializers
from .models import SSHKey, Server

class SSHKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = SSHKey
        fields = '__all__'

class ServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Server
        fields = '__all__'
