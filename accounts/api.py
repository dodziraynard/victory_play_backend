from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from knox.models import AuthToken
from rest_framework.viewsets import ModelViewSet
from django.db.models import Q
from datetime import datetime, timedelta
from accounts.models import Profile, WelfareContributor
from django.contrib.auth import authenticate
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
        user.profile.member_id = Profile.objects.count()
        user.profile.save()

        return Response({
            "profile": ProfileSerializer(user.profile).data,
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
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user and user.is_active:
            profile = Profile.objects.get(user=user)
            return Response({
                "profile": ProfileSerializer(profile).data,
                "token": AuthToken.objects.create(user)[1]
            })
        return Response({"message": "Invalid password or username"}, status=200)


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
        return Response({"profile": data})

    def post(self, request, *args, **kwargs):
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")

        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")

        if new_password and old_password:
            if request.user.check_password(old_password):
                request.user.set_password(new_password)
            else:
                return Response({}, status=403)

        # update user's info
        profile = request.user.profile
        if full_name:
            profile.full_name = full_name
        if mobile:
            profile.mobile = mobile
        if email:
            profile.email = email
        profile.save()

        # Update user's email
        request.user.email = email
        request.user.save()
        print(ProfileSerializer(profile).data)
        return Response({"profile": ProfileSerializer(profile).data})


class WelfareContributorAPI(APIView):
    def get(self, request):
        arrears = WelfareContributor.objects.filter(
            profile=request.user.profile).first().arrears
        if arrears:
            return Response({"user": request.user.pk, "arrears": arrears})
        return Response({}, status=404)
