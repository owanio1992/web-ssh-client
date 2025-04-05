from django.db import models

class SSHKey(models.Model):
    name = models.CharField(max_length=255, unique=True)
    key = models.TextField()

    def __str__(self):
        return self.name

class Server(models.Model):
    site = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    user = models.CharField(max_length=255)
    host = models.CharField(max_length=255)
    ssh_key = models.ForeignKey(SSHKey, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('site', 'name')

    def __str__(self):
        return f"{self.site} - {self.name}"
