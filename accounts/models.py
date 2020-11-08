from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.utils import timezone
from django.conf import settings
from transaction_engine.models import Transaction


class Profile(models.Model):
    member_id = models.CharField(
        max_length=50, unique=True, blank=True, null=True)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    location = models.CharField(max_length=15, blank=True, null=True)
    email = models.CharField(max_length=15, blank=True, null=True)
    image = models.ImageField(
        upload_to="uploads/users", default="avatar.png")
    date = models.DateTimeField(default=timezone.now)
    is_admin = models.BooleanField(default=False)

    class Meta:
        db_table = "profile"

    def get_username(self):
        return self.user.username

    def get_email(self):
        return self.user.email

    def get_image_url(self):
        env = "development" if settings.DEBUG else "production"
        domain = Site.objects.get(name=env).domain
        path = self.image.url
        return f"{domain}{path}"

    def get_formated_date(self):
        return self.date.strftime("%a, %B %d %Y")

    def __str__(self):
        return self.full_name


class WelfareContributor(models.Model):
    profile = models.OneToOneField(
        Profile, on_delete=models.CASCADE, related_name='welfare_contributor')
    date_joined = models.DateTimeField(default=timezone.now)
    arrears = models.DecimalField(
        decimal_places=2, default=0, max_digits=6)
    amount_due = models.DecimalField(
        decimal_places=2, default=0, max_digits=6)
    amount_paid = models.DecimalField(
        decimal_places=2, default=0, max_digits=6)

    class Meta:
        db_table = "welfare_contributors"

    def __str__(self):
        return self.profile.full_name

    def save(self, *args, **kwargs):
        welfares = Transaction.objects.filter(
            type="welfare", user=self.profile.user)
        total_amount_paid = 0
        for item in welfares:
            total_amount_paid += item.amount
        self.amount_paid = total_amount_paid
        self.arrears = self.amount_due - self.amount_paid
        super(WelfareContributor, self).save(*args, **kwargs)


class Leader(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='positions')
    title = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.profile.full_name
