from django.db import models

class User(models.Model):
    """
    Table to keep User with password and username.
    Args:        
        username: string
        password: string
    """
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)