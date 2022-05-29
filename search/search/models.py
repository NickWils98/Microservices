from django.db import models

class Movie(models.Model):
    """
    Table to keep Movies with title, description, year, and runtime.
    Args:        
        title: string
        description: string
        year: string
        runtime: string
    """
    title = models.CharField(max_length=2000)
    description = models.CharField(max_length=2000)
    year = models.CharField(max_length=2000)
    runtime = models.CharField(max_length=2000)