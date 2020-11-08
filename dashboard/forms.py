from django import forms
from .  models import Audio, Video, Pdf
from accounts.models import Leader


class AudioForm(forms.ModelForm):
    class Meta:
        model = Audio
        fields = ["title", "desc", "file", "image"]


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ["title", "desc", "file", "image"]


class PdfForm(forms.ModelForm):
    class Meta:
        model = Pdf
        fields = ["title", "desc", "file", "image"]


class LeaderForm(forms.ModelForm):
    class Meta:
        model = Leader
        fields = ["profile", "title", "department"]
