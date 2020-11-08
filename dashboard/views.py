from django.shortcuts import render, redirect, get_object_or_404
from dashboard.models import (
    Audio,
    Video,
    Pdf,
    Testimony,
    PrayerRequest,
    Feedback,
    Notification,
)
from transaction_engine.models import Transaction
from accounts.models import WelfareContributor, Profile, Leader


def index(request):
    template_name = "dashboard/index.html"
    total_welfare_revenue = 0
    total_welfare_arrears = 0
    welfare_transactions = Transaction.objects.filter(type="welfare")
    welfare_contributors = WelfareContributor.objects.all()

    for item in welfare_transactions:
        total_welfare_revenue += item.amount

    for item in welfare_contributors:
        total_welfare_arrears += item.arrears if item.arrears > 0 else 0

    context = {
        "total_welfare_revenue": total_welfare_revenue,
        "total_welfare_arrears": total_welfare_arrears,
        "totl_contributors": welfare_contributors.count(),
        "users": Profile.objects.all().count(),
        "top_five_contributors": welfare_contributors.order_by("arrears")[:5],
    }
    return render(request, template_name, context)


def welfare(request):
    template_name = "dashboard/welfare.html"
    transactions = Transaction.objects.filter(type="welfare").order_by("-id")
    context = {
        "transactions": transactions
    }
    return render(request, template_name, context)


def new_welfare_member(request):
    template_name = "dashboard/welfare.html"
    member_id = request.POST.get("member_id")
    profile = get_object_or_404(Profile, member_id=member_id)
    WelfareContributor.objects.get_or_create(profile=profile)
    return redirect("dashboard:welfare")


def testimonies(request):
    template_name = "dashboard/testimonies.html"
    context = {
        "testimonies": Testimony.objects.all().order_by("-id", "viewed"),
    }
    return render(request, template_name, context)


def prayer_requests(request):
    template_name = "dashboard/prayer_requests.html"
    context = {
        "prayer_requests": PrayerRequest.objects.all().order_by("-id", "viewed"),
    }
    return render(request, template_name, context)


def audios(request):
    template_name = "dashboard/audios.html"
    context = {
        "audios": Audio.objects.all().order_by("-id"),
    }
    return render(request, template_name, context)


def delete_audio(request, pk):
    audio = get_object_or_404(Audio, pk=pk)
    audio.delete()
    return redirect("dashboard:audios")


def videos(request):
    template_name = "dashboard/videos.html"
    context = {
        "videos": Video.objects.all().order_by("-id"),
    }
    return render(request, template_name, context)


def delete_video(request, pk):
    video = get_object_or_404(Video, pk=pk)
    video.delete()
    return redirect("dashboard:videos")


def pdfs(request):
    template_name = "dashboard/pdfs.html"
    context = {
        "pdfs": Pdf.objects.all().order_by("-id"),
    }
    return render(request, template_name, context)


def delete_pdf(request, pk):
    pdf = get_object_or_404(Pdf, pk=pk)
    pdf.delete()
    return redirect("dashboard:pdfs")


def leaders(request):
    template_name = "dashboard/leaders.html"
    context = {
        "leaders": Leader.objects.all().order_by("-id"),
    }
    return render(request, template_name, context)


def delete_leader(request, pk):
    leader = get_object_or_404(Leader, pk=pk)
    leader.delete()
    return redirect("dashboard:leaders")


def notifications(request):
    template_name = "dashboard/notifications.html"
    notifications = Notification.objects.all().order_by("read", "-id")
    notifications.update(read=True)
    context = {
        "notifications": notifications,
    }
    return render(request, template_name, context)


def profiles(request):
    template_name = "dashboard/profiles.html"
    profiles = Profile.objects.all()
    context = {
        "profiles": profiles,
    }
    return render(request, template_name, context)


def sms(request):
    template_name = "dashboard/sms.html"
    context = {
    }
    return render(request, template_name, context)
