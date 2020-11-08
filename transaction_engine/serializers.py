from rest_framework_jwt.settings import api_settings
from rest_framework import serializers
from .models import Transaction
from accounts.models import Profile


class TransactionSerializer(serializers.ModelSerializer):
    month = serializers.IntegerField(source="get_month", read_only=True)
    year = serializers.IntegerField(source="get_year", read_only=True)
    time_stamp = serializers.CharField(source="time_in_mills", read_only=True)

    class Meta:
        model = Transaction
        fields = "__all__"
