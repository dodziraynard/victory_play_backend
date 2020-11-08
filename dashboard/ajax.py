from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.utils.html import strip_tags
from dashboard.models import (
    Audio,
    Video,
    Pdf,
    Testimony,
    PrayerRequest,
    Feedback
)
from . forms import AudioForm, VideoForm, PdfForm, LeaderForm
from accounts.models import Profile, Leader
from transaction_engine.models import Transaction
import uuid


def update_audio(request, pk):
    message = "Bad Request"
    audio = get_object_or_404(Audio, pk=pk)
    form = AudioForm(request.POST, request.FILES, instance=audio)
    if form.is_valid():
        form.save()
        response_data = {
            "status": "SUCCESS",
        }
        return JsonResponse(response_data)
    else:
        for field, er in form.errors.items():
            message = f"{field.title()}: {strip_tags(er)}"
            break
        response_data = {
            "status": "ERROR",
            "status_message": message,
        }
        return JsonResponse(response_data)


def add_audio(request):
    message = "Bad Request"
    form = AudioForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        response_data = {
            "status": "SUCCESS",
        }
        return JsonResponse(response_data)
    else:
        for field, er in form.errors.items():
            message = f"{field.title()}: {strip_tags(er)}"
            break
        response_data = {
            "status": "ERROR",
            "status_message": message,
        }
        return JsonResponse(response_data, status=400)


def update_video(request, pk):
    message = "Bad Request"
    video = get_object_or_404(Video, pk=pk)
    form = VideoForm(request.POST, request.FILES, instance=video)
    if form.is_valid():
        form.save()
        response_data = {
            "status": "SUCCESS",
        }
        return JsonResponse(response_data)
    else:
        for field, er in form.errors.items():
            message = f"{field.title()}: {strip_tags(er)}"
            break
        response_data = {
            "status": "ERROR",
            "status_message": message,
        }
        return JsonResponse(response_data)


def add_video(request):
    message = "Bad Request"
    form = VideoForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        response_data = {
            "status": "SUCCESS",
        }
        return JsonResponse(response_data)
    else:
        for field, er in form.errors.items():
            message = f"{field.title()}: {strip_tags(er)}"
            break
        response_data = {
            "status": "ERROR",
            "status_message": message,
        }
        return JsonResponse(response_data, status=400)


def update_pdf(request, pk):
    message = "Bad Request"
    pdf = get_object_or_404(Pdf, pk=pk)
    form = PdfForm(request.POST, request.FILES, instance=pdf)
    if form.is_valid():
        form.save()
        response_data = {
            "status": "SUCCESS",
        }
        return JsonResponse(response_data)
    else:
        for field, er in form.errors.items():
            message = f"{field.title()}: {strip_tags(er)}"
            break
        response_data = {
            "status": "ERROR",
            "status_message": message,
        }
        return JsonResponse(response_data)


def add_pdf(request):
    message = "Bad Request"
    form = PdfForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        response_data = {
            "status": "SUCCESS",
        }
        return JsonResponse(response_data)
    else:
        for field, er in form.errors.items():
            message = f"{field.title()}: {strip_tags(er)}"
            break
        response_data = {
            "status": "ERROR",
            "status_message": message,
        }
        return JsonResponse(response_data, status=400)


def add_transaction(request):
    member_id = request.POST.get("member_id")
    amount = request.POST.get("amount")

    profile = get_object_or_404(Profile, member_id=member_id)
    transaction = Transaction.objects.create(amount=amount, user=profile.user, transaction_id=str(
        uuid.uuid4()), type="welfare", mode="manual")

    response_data = {
        "status": "SUCCESS",
        "status_message": "New transaction record added!",
    }
    return JsonResponse(response_data, status=200)


def update_leader(request, pk):
    message = "Bad Request"
    leader = get_object_or_404(Leader, pk=pk)
    member_id = request.POST.get("member_id")
    form = LeaderForm(request.POST, instance=leader)
    if form.is_valid():
        leader = form.save()
        Leader.objects.filter(pk=pk).update(
            profile=Profile.objects.get(member_id=member_id))
        response_data = {
            "status": "SUCCESS",
        }
        return JsonResponse(response_data)
    else:
        for field, er in form.errors.items():
            message = f"{field.title()}: {strip_tags(er)}"
            break
        response_data = {
            "status": "ERROR",
            "status_message": message,
        }
        return JsonResponse(response_data)


def add_leader(request):
    title = request.POST.get("title")
    department = request.POST.get("department")
    member_id = request.POST.get("member_id")
    profile = get_object_or_404(Profile, member_id=member_id)
    Leader.objects.get_or_create(
        profile=profile, department=department, title=title)
    response_data = {
        "status": "SUCCESS",
    }
    return JsonResponse(response_data)
