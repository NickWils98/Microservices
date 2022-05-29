from django.db import models

class Group(models.Model):
    """
    Table to keep all groups with a name.
    Args:
        name: string
    """
    name = models.CharField(max_length=200)
    

class GroupUser(models.Model):
    """
    Table to keep members of a group with groupname and username.
    Args:        
        groupname: string
        username: string
    """
    groupname = models.CharField(max_length=200)
    username = models.CharField(max_length=200)