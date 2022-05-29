from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ViewSet):
    def list(self):
        """
        Return a list of all the entries in the User table for test purposes.
        Returns:
            list : return a list with all the entries with status 200
        """
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):        
        """
        Add an entry in the User table with user and password.
        Only if username is not already in the table.
        Args:
            request (json): has keys: username and password

        Returns:
            bool: On succes True with status 201.
                  On failure False with status 400
        """
        # check if user is already in the table
        if User.objects.filter(username=request.data["username"]).exists():
            return Response({"response":False}, status=status.HTTP_400_BAD_REQUEST)

        # add user to table
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"response":True}, status=status.HTTP_201_CREATED)

    def retrieve(self, request):
        """
        Check if the user is in the database with the correct password for login.
        Args:
            request (json): has keys: username, password

        Returns:
            bool: If friends True with status 200.
                  Else False with status 400
        """
        # check if username an password are in the table
        if User.objects.filter(username=request.data["username"], password=request.data["password"]).exists():
            return Response({"response":True}, status=status.HTTP_201_CREATED)
        return Response({"response":False}, status=status.HTTP_400_BAD_REQUEST)


    def exists(self, request):
        """
        Check if the user is in the database.
        Args:
            request (json): has key: username

        Returns:
            bool: If friends True with status 200.
                  Else False with status 400
        """
        # check if user is in the database
        if User.objects.filter(username=request.data["username"]).exists():
            return Response({"response":True}, status=status.HTTP_200_OK)
        return Response({"response":False}, status=status.HTTP_400_BAD_REQUEST)