from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from pathlib import Path
from django.utils import timezone
from django.conf import settings
import os


def content_file_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (instance.title, ext)
    return os.path.join('uploads', filename)


class ResourceMixin(models.Model):
    title = models.CharField(max_length=100)
    desc = models.TextField(null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)
    image = models.ImageField(
        upload_to="uploads/images", blank=True, null=True)
    file = models.FileField(upload_to=content_file_name)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    def get_readable_date(self):
        return self.date.strftime("%a, %B %d. %I:%M %p")

    def get_file_url(self):
        env = "development" if settings.DEBUG else "production"
        domain = Site.objects.get(name=env).domain
        path = self.file.url
        return f"{domain}{path}"

    def get_image_url(self):
        env = "development" if settings.DEBUG else "production"
        domain = Site.objects.get(name=env).domain
        path = self.image.url
        return f"{domain}{path}"

    def save(self, *args, **kwargs):
        ext = self.file.url.split('.')[-1]
        if not "."+ext in self.title:
            self.title = f"{self.title}.{ext}"
        super(ResourceMixin, self).save(*args, **kwargs)


class Audio(ResourceMixin):
    class Meta:
        db_table = "audio"


class Video(ResourceMixin):
    class Meta:
        db_table = "video"


class Pdf(ResourceMixin):
    class Meta:
        db_table = "pdf"


class Testimony(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="testimonies")
    testimony = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    viewed = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Testimonies"
        db_table = "testimonies"

    def __str__(self):
        return self.testimony


class PrayerRequest(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="prayer_requests")
    request = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    viewed = models.BooleanField(default=False)

    class Meta:
        db_table = "prayer_requests"

    def __str__(self):
        return self.user.username


class Feedback(models.Model):
    user = models.ForeignKey(User, null=True, blank=True,
                             on_delete=models.SET_NULL, related_name="feedbacks")
    feedback = models.TextField()
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "feedbacks"

    def __str__(self):
        return self.feedback


class Notification(models.Model):
    message = models.TextField()
    title = models.CharField(max_length=500)
    time_stamp = models.DateTimeField(default=timezone.now)
    icon = models.ImageField(upload_to="uploads/images", blank=True, null=True)
    read = models.BooleanField(default=False)
    redirect_url = models.URLField(blank=True, null=True)

    class Meta:
        db_table = "notifications"

    def __str__(self):
        return self.message


class Config(models.Model):
    site_name = models.CharField(max_length=200)
    welfare_rate = models.DecimalField(decimal_places=2, max_digits=3)
    logo = models.ImageField(upload_to="uploads/images", blank=True, null=True)

    class Meta:
        db_table = "config"

    def __str__(self):
        return self.site_name


class SMS(models.Model):
    message = models.TextField()
    number = models.CharField(max_length=12)
    failed = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.number
