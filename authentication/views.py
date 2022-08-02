from django.contrib.auth.hashers import check_password
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import exceptions

from authentication.models import User
from helpers import IsSuperUser
from authentication.serializers import ChangePasswordSerializer, UserRegisterSerializer,\
    ProfileSerializer, UpdateUserSerializer


class RegisterAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            data = {'detail': user.name + ' registered successfully!'}

            return Response(data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


def validate_user(attrs):
    try:
        user = User.objects.get(username=attrs['username'])

        check = check_password(attrs['password'], user.password)
        if check:
            return user
        else:
            raise exceptions.AuthenticationFailed('Invalid Password')
    except User.DoesNotExist:
        raise exceptions.AuthenticationFailed('No such user')


def generate_token(user):
    try:
        Token.objects.get(user=user).delete()
    except:
        pass
    return Token.objects.create(user=user)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        user = validate_user(request.data)
        serializer = ProfileSerializer(user)
        data = serializer.data

        try:
            token = generate_token(user)
            data.update({'token': token.key})
            return Response(data, status=HTTP_200_OK)
        except HTTP_400_BAD_REQUEST:
            return Response("Bad Request", status=HTTP_400_BAD_REQUEST)


class LoginSuperUserAPIView(APIView):
    permission_classes = (IsSuperUser,)

    def post(self, request):
        user = validate_user(request.data)
        serializer = ProfileSerializer(user)
        data = serializer.data

        try:
            token = generate_token(user)
            data.update({'token': token.key})
            return Response(data, status=HTTP_200_OK)
        except HTTP_400_BAD_REQUEST:
            return Response("Bad Request", status=HTTP_400_BAD_REQUEST)


class ProfileAPIView(APIView):
    def get(self, request):
        try:
            user = request.user
            serializer = ProfileSerializer(user)
            return Response(serializer.data, status=HTTP_200_OK)
        except:
            return Response("Bad Request", status=HTTP_400_BAD_REQUEST)


class ChangePasswordAPIView(APIView):
    # Uncomment these lines if you don't want to use custom put method
    # and change APIView class parameter to UpdateAPIView
    # queryset = User.objects.all()
    # serializer_class = ChangePasswordSerializer

    # Comment this put function if you don't want to use custom put method
    def put(self, request):
        user = request.user

        serializer = ChangePasswordSerializer(data=request.data, context={'user': user})
        if serializer.is_valid():
            serializer.update(user, request.data)

            data = {'detail': 'Password changed successfully!'}

            return Response(data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class UpdateFCMTokenAPIView(APIView):
    def put(self, request):
        user = request.user

        serializer = UpdateUserSerializer(instance=user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.update(user, request.data)

            data = {'message': 'FCM token updated successfully!'}

            return Response(data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
