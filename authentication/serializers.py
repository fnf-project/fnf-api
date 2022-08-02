from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password

from authentication.models import User


class UserRegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

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
            'subsidy_date',
            'is_shopkeeper'
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


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        user = self.context['user']
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is not correct")
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()

        return instance


class UpdateUserSerializer(serializers.ModelSerializer):

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
            'subsidy_date',
            'is_shopkeeper',
            'fcm_token'
        )
        read_only_fields = ('id', 'username', 'name')
        extra_kwargs = {
            'fcm_token': {'required': True},
        }

    def update(self, instance, validated_data):
        instance.family_members = validated_data.get('family_members', instance.family_members)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.address = validated_data.get('address', instance.address)
        instance.subsidy_amount = validated_data.get('subsidy_amount', instance.subsidy_amount)
        instance.is_shopkeeper = validated_data.get('is_shopkeeper', instance.is_shopkeeper)
        instance.fcm_token = validated_data.get('fcm_token', instance.fcm_token)

        instance.save()
        return instance
