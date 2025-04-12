from django.contrib import admin
from .models import SSHKey, Server, Role, UserRole
from django.db import models

class SSHKeyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'key_content')

class ServerAdmin(admin.ModelAdmin):
    list_display = ('id', 'site_name', 'server_name', 'user', 'host', 'ssh_key')

class RoleAdmin(admin.ModelAdmin):
    filter_horizontal = ('permissions',)
    list_display = ('id', 'name')

class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', )
    filter_horizontal = ('roles',)

# Register your models here.
admin.site.register(SSHKey, SSHKeyAdmin)
admin.site.register(Server, ServerAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(UserRole, UserRoleAdmin)
