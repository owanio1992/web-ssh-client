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
