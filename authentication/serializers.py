from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from authentication.models import User


class UserRegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'username',
            'name',
            'mobile_number',
            'address',
            'location',
            'password')

    def create(self, validated_data):
        password = make_password(validated_data.get('password'))
        validated_data.update({'password': password})
        return super(UserRegisterSerializer, self).create(validated_data)


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'name',
            'mobile_number',
            'address',
            'location')
