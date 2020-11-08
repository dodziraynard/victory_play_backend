from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from knox.models import AuthToken
from rest_framework.viewsets import ModelViewSet
from django.db.models import Q
from datetime import datetime, timedelta
from dashboard.models import (
    Audio,
    Video,
    Pdf,
    Testimony,
    PrayerRequest,
    Feedback,
)

from . serializers import (
    VideoSerializer,
    PdfSerializer,
    AudioSerializer,
    TestimonySerializer,
    PrayerRequestSerializer,
    FeedbackSerializer
)


class VideosAPI(APIView):
    serializer_class = VideoSerializer

    def get(self, request, *args, **kwargs):
        query = request.GET.get("query")
        videos = Video.objects.all().order_by("-id")
        if query:
            videos = videos.filter(
                Q(title__icontains=query) |
                Q(desc__icontains=query)
            )
        data = self.serializer_class(videos, many=True).data
        return Response({"videos": data})


class PdfsAPI(APIView):
    serializer_class = PdfSerializer

    def get(self, request, *args, **kwargs):
        query = request.GET.get("query")
        materials = Pdf.objects.all().order_by("-id")
        if query:
            materials = materials.filter(
                Q(title__icontains=query) |
                Q(desc__icontains=query)
            )
        data = self.serializer_class(materials, many=True).data
        return Response({"pdfs": data})


class AudiosAPI(APIView):
    serializer_class = AudioSerializer

    def get(self, request):
        query = request.GET.get("query")
        audios = Audio.objects.all().order_by("-id")
        if query:
            audios = audios.filter(
                Q(title__icontains=query) |
                Q(desc__icontains=query)
            )
        data = self.serializer_class(audios, many=True).data
        return Response({"audios": data})


class TestimonyAPI(ModelViewSet):
    serializer_class = TestimonySerializer

    def get_queryset(self):
        return self.request.user.testimonies

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PrayerRequestAPI(ModelViewSet):
    serializer_class = PrayerRequestSerializer

    def get_queryset(self):
        return self.request.user.prayer_requests

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FeedbackAPI(ModelViewSet):
    serializer_class = FeedbackSerializer

    def get_queryset(self):
        return Feedback.objects.all()

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
