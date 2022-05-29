from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Friend
from .serializers import FriendSerializer
import requests



class FriendViewSet(viewsets.ViewSet):
    """
    API for friend microservice
    """
    def list(self):
        """
        Return a list of all the entries in the Friend table for test purposes.
        Returns:
            list : return a list with all the entries with status 200
        """
        friends = Friend.objects.all()
        serializer = FriendSerializer(friends, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """
        Add an entry in the Friend table with current user and friend.
        Only if friend exists and not already friends.
        Args:
            request (json): has keys: username and friendname

        Returns:
            bool: On succes True with status 201.
                  On failure False with status 400/500
        """
        data = request.data
        user1 = {'username':data["friendname"]}
        # if username and friendname are the same return False
        if data["username"] == data["friendname"]:
            return Response({"response":False}, status=status.HTTP_400_BAD_REQUEST)
        
        # check if friend exits with API call to the login microservice
        try:
            success = requests.get("http://login:8001/api/user_exists", json=user1).json()["response"]
            if not success:
                return Response({"response":False}, status=status.HTTP_400_BAD_REQUEST)
        except:
                return Response({"response":False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        # check if friend is already in table
        if Friend.objects.filter(username=data["username"], friendname=data["friendname"]).exists():
            return Response({"response":False}, status=status.HTTP_400_BAD_REQUEST)
        # check if friend is already in table but with username and friendname switched
        if Friend.objects.filter(username=data["friendname"], friendname=data["username"]).exists():
            return Response({"response":False}, status=status.HTTP_400_BAD_REQUEST)
        
        # add user-friend to table
        serializer = FriendSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        # add reversed friend-user to the table
        reversed_data = {"username":data["friendname"], "friendname":data["username"]}
        serializer = FriendSerializer(data=reversed_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"response":True}, status=status.HTTP_201_CREATED)

    def exists(self, request):
        """
        Check if the two users are friends in the database.
        Args:
            request (json): has keys: username and friendname

        Returns:
            bool: If friends True with status 200.
                  Else False with status 400
        """
        success = False
        data = {"username":request.data["username"], "friendname":request.data["friendname"]}
        # check if friend is already in table
        if Friend.objects.filter(username=data["username"], friendname=data["friendname"]).exists():
            success = True
        # check if friend is already in table but with username and friendname switched
        if Friend.objects.filter(username=data["friendname"], friendname=data["username"]).exists():
            success = True
        if success:
            return Response({"response":True}, status=status.HTTP_200_OK)
        return Response({"response":False}, status=status.HTTP_400_BAD_REQUEST)