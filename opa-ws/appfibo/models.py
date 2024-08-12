from django.db import models

class ConnectedUser(models.Model):
    username = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.username} | {self.is_active}'