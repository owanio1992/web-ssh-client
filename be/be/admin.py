from django.contrib import admin
from .models import SSHKey, Server, Role, UserRole
from django.db import models

class RoleAdmin(admin.ModelAdmin):
    filter_horizontal = ('permissions',)

# Register your models here.
admin.site.register(SSHKey)
admin.site.register(Server)
admin.site.register(Role, RoleAdmin)
admin.site.register(UserRole)
