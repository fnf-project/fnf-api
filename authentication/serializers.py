from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from authentication.models import User


class UserRegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'username',
            'password',
            'name',
            'family_members',
            'phone_number',
            'address',
            'subsidy_amount',
            'subsidy_percentage',
            'starting_date',
            'subsidy_date'
        )

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
            'family_members',
            'phone_number',
            'address',
            'subsidy_amount',
            'subsidy_percentage',
            'starting_date',
            'subsidy_date'
        )
