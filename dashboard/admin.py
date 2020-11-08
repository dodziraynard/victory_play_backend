from django.contrib import admin
from dashboard.models import (
    Audio,
    Video,
    Pdf,
    Testimony,
    PrayerRequest,
    Feedback,
    Config,
    Notification,
)

admin.site.register(Audio)
admin.site.register(Video)
admin.site.register(Pdf)
admin.site.register(Testimony)
admin.site.register(PrayerRequest)
admin.site.register(Feedback)
admin.site.register(Config)
admin.site.register(Notification)
