from django.db import models

class SSHKey(models.Model):
    name = models.CharField(max_length=255)
    key_content = models.TextField()

    def __str__(self):
        return self.name

class Server(models.Model):
    site_name = models.CharField(max_length=200)
    server_name = models.CharField(max_length=200)
    user = models.CharField(max_length=200)
    host = models.CharField(max_length=200)
    ssh_key = models.ForeignKey(SSHKey, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.site_name} - {self.server_name}"

class Role(models.Model):
    name = models.CharField(max_length=255, unique=True)
    permissions = models.ManyToManyField(Server, blank=True)

    def __str__(self):
        return self.name

class UserRole(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    roles = models.ManyToManyField(Role, blank=True)

    def __str__(self):
        return f"{self.user.username} - {', '.join([role.name for role in self.roles.all()])}"
