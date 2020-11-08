from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from knox.models import AuthToken
from rest_framework.viewsets import ModelViewSet
from django.db.models import Q
from datetime import datetime, timedelta
from accounts.models import Profile, WelfareContributor

from . serializers import (
    UserSerializer,
    RegisterSerializer,
    LoginSerializer,
    ProfileSerializer,
)


# Register API
class RegisterAPI(generics.GenericAPIView):
    """
    User registration endpoint
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        full_name = request.POST.get("full_name")
        mobile = request.POST.get("mobile")

        user.profile.full_name = full_name
        user.profile.mobile = mobile
        user.profile.save()

        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


# Login API
class LoginAPI(generics.GenericAPIView):
    """
    User login endpoint
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        profile = Profile.objects.get(user=user)
        return Response({
            "profile": ProfileSerializer(profile).data,
            "token": AuthToken.objects.create(user)[1]
        })


# Get User API
class UserAPI(APIView):
    """
    User endpoint to retrieve and update an authenticated user.
    """

    def get(self, request):
        user = request.user
        data = UserSerializer(user).data
        return Response({"user": data})

    def patch(self, request, *args, **kwargs):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        username = request.data.get("username")
        email = request.data.get("email")

        if email:
            user.email = email
        if username:
            user.username = username
        user.save()

        if new_password and old_password:
            if user.check_password(old_password):
                user.set_password(new_password)

            else:
                errors = {"detail": "Invalid Old Password"}
                return Response(errors, status=status.HTTP_403_FORBIDDEN)

        data = UserSerializer(user).data
        return Response({"user": data})


# UserProfile API
class UserProfileAPI(APIView):
    """
    API endpoint by which an authenticated user can view his/her profile
    """
    serializer_class = ProfileSerializer

    def get(self, request):
        data = self.serializer_class(request.user.profile).data
        return Response({"profile": [data]})

    def post(self, request, *args, **kwargs):
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")

        # update user's info
        profile = request.user.profile
        profile.full_name = full_name
        profile.mobile = mobile
        profile.save()

        # Update user's email
        request.user.email = email
        request.user.save()

        data = self.serializer_class(request.user.profile).data
        return Response({"profile": [data]})


class WelfareContributorAPI(APIView):
    def get(self, request):
        arrears = WelfareContributor.objects.get(
            profile=request.user.profile).arrears
        return Response({"user": request.user.pk, "arrears": arrears})
