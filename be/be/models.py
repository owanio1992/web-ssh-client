from django.db import models

class SSHKey(models.Model):
    name = models.CharField(max_length=255)
    key_content = models.TextField()

    def __str__(self):
        return self.name
