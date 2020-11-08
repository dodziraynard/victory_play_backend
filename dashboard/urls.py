from django.urls import path, include
from rest_framework import routers
from . import api, views, ajax

app_name = "dashboard"

# API
router = routers.DefaultRouter()
router.register("testimonies", api.TestimonyAPI, 'testimonies')
router.register("prayer-requests", api.PrayerRequestAPI, 'prayer_request')
router.register("feedback", api.FeedbackAPI, 'feedback')
urlpatterns = [
    path('api/v1/', include(router.urls)),
    path("api/v1/videos", api.VideosAPI.as_view()),
    path("api/v1/pdfs", api.PdfsAPI.as_view()),
    path("api/v1/audios", api.AudiosAPI.as_view(), name="audios"),
]

# AJAX
urlpatterns += {
    path("ajax/audio/<int:pk>/update", ajax.update_audio, name="update_audio"),
    path("ajax/audio/add", ajax.add_audio, name="add_audio"),

    path("ajax/video/<int:pk>/update", ajax.update_video, name="update_video"),
    path("ajax/video/add", ajax.add_video, name="add_video"),

    path("ajax/pdf/<int:pk>/update", ajax.update_pdf, name="update_pdf"),
    path("ajax/pdf/add", ajax.add_pdf, name="add_pdf"),

    path("ajax/transaction/add", ajax.add_transaction, name="add_transaction"),

    path("ajax/leader/<int:pk>/update", ajax.update_leader, name="update_leader"),
    path("ajax/leader/add", ajax.add_leader, name="add_leader"),
}

# VIEWS
urlpatterns += {
    path("", views.index, name="index"),
    path("welfare", views.welfare, name="welfare"),
    path("new-welfare-member", views.new_welfare_member, name="new_welfare_member"),

    path("testimonies", views.testimonies, name="testimonies"),
    path("prayer-requests", views.prayer_requests, name="prayer_requests"),

    path("audios", views.audios, name="audios"),
    path("audio/<int:pk>/delete", views.delete_audio, name="delete_audio"),

    path("videos", views.videos, name="videos"),
    path("video/<int:pk>/delete", views.delete_video, name="delete_video"),

    path("pdfs", views.pdfs, name="pdfs"),
    path("pdf/<int:pk>/delete", views.delete_pdf, name="delete_pdf"),

    path("leaders", views.leaders, name="leaders"),
    path("leader/<int:pk>/delete", views.delete_leader, name="delete_leader"),

    path("notifications", views.notifications, name="notifications"),
    path("profiles", views.profiles, name="profiles"),
    path("sms", views.sms, name="sms"),
}
