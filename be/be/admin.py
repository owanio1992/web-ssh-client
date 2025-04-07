from django.contrib import admin
from .models import SSHKey, Server, Role, UserRole

# Register your models here.
admin.site.register(SSHKey)
admin.site.register(Server)
admin.site.register(Role)
admin.site.register(UserRole)
