from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from knox.models import AuthToken
from rest_framework.viewsets import ModelViewSet
from django.db.models import Q
from datetime import datetime, timedelta
from .models import Transaction

from . serializers import TransactionSerializer


class TransactionAPI(APIView):
    serializer_class = TransactionSerializer

    def get(self, request, *args, **kwargs):
        type = request.GET.get("type")
        transaction = Transaction.objects.filter(
            user=request.user).order_by("-id")
        if type:
            transaction = transaction.filter(
                Q(type__icontains=type)
            )
        data = self.serializer_class(transaction, many=True).data
        return Response({"transactions": data})


class MakeTransactionAPI(APIView):
    serializer_class = TransactionSerializer

    def post(self, request, *args, **kwargs):
        type = request.POST.get("type")
        user_id = request.POST.get("user_id")
        full_name = request.POST.get("full_name")
        mobile = request.POST.get("mobile")
        amount = request.POST.get("amount")
        print(type, user_id, full_name, mobile, amount)
        return Response({"transactions": "data"})
