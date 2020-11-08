from rest_framework_jwt.settings import api_settings
from rest_framework import serializers
from dashboard.models import (
    Audio,
    Video,
    Pdf,
    Testimony,
    PrayerRequest,
    Feedback
)
from accounts.models import Profile


class VideoSerializer(serializers.ModelSerializer):
    file = serializers.URLField(source="get_file_url", read_only=True)
    image = serializers.URLField(source="get_image_url", read_only=True)
    date = serializers.CharField(source="get_readable_date", read_only=True)

    class Meta:
        model = Video
        fields = "__all__"


class PdfSerializer(serializers.ModelSerializer):
    file = serializers.URLField(source="get_file_url", read_only=True)
    image = serializers.URLField(source="get_image_url", read_only=True)
    date = serializers.CharField(source="get_readable_date", read_only=True)

    class Meta:
        model = Pdf
        fields = "__all__"


class AudioSerializer(serializers.ModelSerializer):
    file = serializers.URLField(source="get_file_url", read_only=True)
    date = serializers.CharField(source="get_readable_date", read_only=True)
    image = serializers.URLField(source="get_image_url", read_only=True)

    class Meta:
        model = Audio
        fields = "__all__"


class TestimonySerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimony
        fields = ["testimony"]


class PrayerRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrayerRequest
        fields = ["request"]


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ["feedback"]
