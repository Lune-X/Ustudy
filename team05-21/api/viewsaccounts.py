from django.shortcuts import get_list_or_404, get_object_or_404

from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework.permissions import AllowAny, IsAuthenticated
from api import serializeraccounts
from api.permissions import IsAdminOrSelf

from api.serializeraccounts import UserSerializer
from Accounts import models

from django.contrib import auth

class UserViewSet(viewsets.ModelViewSet):
    queryset = models.MyUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrSelf]

    def _get_my_account(self, request):
        return get_object_or_404(self.queryset, id=request.user.id)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def signup(self, request):
        # Usage: POST to /api/user/signup
        # Front-end sends: JSON object: { username: string, email: string, password: string }
        # Back-end sends: Status: HTTP 200 (sucess) or error

        data = request.data.copy()

        username = request.data['username']
        email = request.data['email']
        password = request.data['password']

        try:
            user = models.MyUser.objects.create_user(username = username, email = email, password = password)
        except Exception as e:
            return Response({'message': 'error trying to create new user!', 'exception': str(e) }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({'message': 'successfully created new user!'}, status=status.HTTP_200_OK)


    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        # Usage: POST to /api/user/login
        # Front-end sends: JSON object: { username: string, password: string }
        # Back-end sends: Authenticated response (set session cookie ID) (status 200 if success, or else error)

        username = request.data['username']
        password = request.data['password']
        
        user = auth.authenticate(request, username=username, password=password)

        if user is None:
            return Response({'message': 'error trying to log user in!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        auth.login(request, user)
        return Response({'message': 'successfully logged user in!'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def logout(self, request):
        # Usage: POST to /api/user/logout
        # Front-end sends: Nothing
        # Back-end sends: Status: HTTP 200 if success, else error

        auth.logout(request)
        return Response({'message': 'logged out!'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def get_me(self, request):
        # Usage: GET to /api/user/get_me
        # Front-end sends: Nothing
        # Back-end sends: { username: String, email: String, year_of_study: Int, course: { id: String, name: String } }

        me = self._get_my_account(request)

        me_serialized = serializeraccounts.UserSerializer(me)
        return Response(me_serialized.data, status=status.HTTP_200_OK)


    # bad, unvalidated code coming up

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def set_username(self, request):
        # Usage: POST to /api/user/set_username
        # Front-end sends: { username: String }
        # Back-end sends: HTTP Status 200 if success, else error
        
        me = self._get_my_account(request)

        me.username = request.data['username']
        me.save()

        return Response({'message': 'set username'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def set_password(self, request):
        # Usage: POST to /api/user/set_password
        # Front-end sends: { password: String }
        # Back-end sends: HTTP Status 200 if success, else error

        me = self._get_my_account(request)

        me.set_password(request.data['password'])
        me.save()

        return Response({'message': 'set password'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def set_email(self, request):
        # Usage: POST to /api/user/set_email
        # Front-end sends: { email: String }
        # Back-end sends: HTTP Status 200 if success, else error

        me = self._get_my_account(request)

        me.email = request.data['email']
        me.save()

        return Response({'message': 'set email'}, status=status.HTTP_200_OK)

    

