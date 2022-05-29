from django.db import models

class Friend(models.Model):
    """
    Table to keep friends with two users.
    Args:        
        username: string
        friendname: string
    """
    username = models.CharField(max_length=200)
    friendname = models.CharField(max_length=200)
    