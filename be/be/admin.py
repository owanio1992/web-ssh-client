from django.contrib import admin
from .models import SSHKey, Server

admin.site.register(SSHKey)
admin.site.register(Server)
