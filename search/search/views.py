from os import stat
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Movie


class MovieViewSet(viewsets.ViewSet):
    def list(self, request):
        """
        Return a list of all the titles in the Movie table.
        Returns:
            list : return a list with all the titles with status 200
        """
        movies = Movie.objects.values("title")
        # make the formate list of strings instead of list of lists
        movies_list = [x["title"] for x in movies]
        return Response({"response":movies_list}, status=status.HTTP_200_OK)
