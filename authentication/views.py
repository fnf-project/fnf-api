from django.contrib.auth.hashers import check_password
from django.http import Http404
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from authentication.models import User
from authentication.serializers import UserRegisterSerializer, ProfileSerializer


class RegisterAPIView(APIView):

    permission_classes = (AllowAny,)

    serializer_class = UserRegisterSerializer

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()

            data['success'] = True
            data['message'] = user.name + ' registered successfully!'

            return Response(data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):

    permission_classes = (AllowAny,)

    def validate_user(self, username, password):
        try:
            user = User.objects.get(username=username)
            check = check_password(password, user.password)
            if check:
                return user
            else:
                raise Http404
        except User.DoesNotExist:
            raise Http404

    def generate_token(self, user):
        try:
            Token.objects.get(user=user).delete()
        except:
            pass
        return Token.objects.create(user=user)

    def post(self, request):
        data = request.data
        user = self.validate_user(data['username'], data['password'])
        serializer = ProfileSerializer(user)
        data = serializer.data

        try:
            token = self.generate_token(user)
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
