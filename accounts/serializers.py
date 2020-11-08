from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from . models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="get_username", read_only=True)
    email = serializers.CharField(source="get_email", read_only=True)
    image = serializers.URLField(source="get_image_url", read_only=True)
    date = serializers.URLField(source="get_formated_date", read_only=True)

    class Meta:
        model = Profile
        fields = "__all__"


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "is_superuser"]


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField()
    mobile = serializers.CharField()

    class Meta:
        model = User
        fields = ["id", "username", "password", "full_name", "mobile"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        validated_data.pop('id', None)
        password = validated_data.pop('password', None)
        full_name = validated_data.pop('full_name', None)
        mobile = validated_data.pop('mobile', None)

        user = self.Meta.model(**validated_data)
        if password:
            user.set_password(password)
            user.save()
            profile = Profile.objects.create(user=user)
        return user


# Login Serializer
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")
