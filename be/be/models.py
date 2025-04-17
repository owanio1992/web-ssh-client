import os
from django.db import models
from cryptography.fernet import Fernet
from django.conf import settings

def generate_encryption_key():
    """
    Generates a new encryption key.
    """
    return Fernet.generate_key()

def get_fernet():
    """
    Retrieves the Fernet instance using the encryption key from settings.
    """
    encryption_key = settings.ENCRYPTION_KEY
    if not encryption_key:
        raise ValueError("Encryption key not found in settings.")
    return Fernet(encryption_key)

class SSHKey(models.Model):
    name = models.CharField(max_length=255)
    key_content = models.TextField()

    def save(self, *args, **kwargs):
        fernet = get_fernet()
        self.key_content = fernet.encrypt(self.key_content.encode()).decode()
        super().save(*args, **kwargs)

    def decrypt_key(self):
        fernet = get_fernet()
        return fernet.decrypt(self.key_content.encode()).decode()

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
