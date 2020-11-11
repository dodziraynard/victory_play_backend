from django.urls import path, include
from . import api, views

app_name = "accounts"

urlpatterns = [
    path("api/v1/auth/profile", api.UserProfileAPI.as_view()),
    path("api/v1/welfare-arrears",
         api.WelfareContributorAPI.as_view()),

    # users
    path('api/v1/auth/register', api.RegisterAPI.as_view()),
    path('api/v1/auth/login', api.LoginAPI.as_view()),
    path('api/v1/auth/user', api.UserAPI.as_view()),
]

urlpatterns += [
    path("auth/login", views.UserLogin.as_view(), name="login"),
    path("auth/logout", views.logout_user, name="logout"),
]
