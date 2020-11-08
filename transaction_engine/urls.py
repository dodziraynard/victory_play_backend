from django.urls import path, include
from rest_framework import routers
from . import api


urlpatterns = [
    path("api/v1/transactions", api.TransactionAPI.as_view()),
    path("api/v1/make-transaction/", api.MakeTransactionAPI.as_view()),
]
