from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Group, GroupUser
from .serializers import GroupSerializer, GroupUserSerializer
import requests


class GroupViewSet(viewsets.ViewSet):
    def list(self, request):
        """
        Return a list of all the entries in the GroupUser table for test purposes.
        Returns:
            list : return a list with all the entries with status 200
        """
        groups = GroupUser.objects.all()
        serializer = GroupUserSerializer(groups, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):        
        """
        Add an entry in the Group table with the groupname.
        Only if groupname is not in the table already.
        Add the user as member of the group in the GroupUser table.
        Args:
            request (json): has keys: groupname, username

        Returns:
            bool: On succes True with status 201.
                  On failure False with status 400
        """
        # check if groupname is already a group
        data = {"name": request.data["groupname"]}
        if Group.objects.filter(name=data["name"]).exists():
            return Response({"response":False}, status=status.HTTP_400_BAD_REQUEST)
        # add group to table
        serializer = GroupSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        # add user as member of group in table
        serializer2 = GroupUserSerializer(data=request.data)
        serializer2.is_valid(raise_exception=True)
        serializer2.save()        

        return Response({"response":True}, status=status.HTTP_201_CREATED)
 
    def add_to_group(self, request):
        """
        Add an friend as member of group in GroupUser table.
        Only if the group exists, user and friend are friends, user is in the group and friend is not yet a member.
        Args:
            request (json): has keys: username, friendname and groupname

        Returns:
            bool: On succes True with status 201.
                  On failure False with status 400/500
        """
        data = {"name": request.data["groupname"]}        
        # check if group exists
        if not Group.objects.filter(name=data["name"]).exists():
            return Response({"response":False}, status=status.HTTP_400_BAD_REQUEST)
        user_friend = {"username":request.data["username"], "friendname":request.data["friend_username"]}
        
        # check if friend and user are friends with API call to the friend microservice
        try:
            success = requests.get("http://friend:8002/api/friend_exists", json=user_friend).json()["response"]
            if not success:
                return Response({"response":False}, status=status.HTTP_400_BAD_REQUEST)
        except:
                return Response({"response":False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        group_friend_data = {"groupname":request.data["groupname"], "username":request.data["friend_username"]}
        
        # check if user is in the group
        if not GroupUser.objects.filter(groupname=data["name"], username=request.data["username"]).exists():
            return Response({"response":False}, status=status.HTTP_400_BAD_REQUEST)

        # check if friend is not yet in the group
        if GroupUser.objects.filter(groupname=data["name"], username=request.data["friend_username"]).exists():
            return Response({"response":False}, status=status.HTTP_400_BAD_REQUEST)
        
        # add friend as member of group
        serializer = GroupUserSerializer(data=group_friend_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"response":True}, status=status.HTTP_201_CREATED)
