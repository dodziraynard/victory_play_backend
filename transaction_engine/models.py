from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Transaction(models.Model):
    amount = models.DecimalField(decimal_places=2, max_digits=6)
    time_stamp = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    transaction_id = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    mode = models.CharField(max_length=50, default="manual")

    class Meta:
        db_table = "transaction"

    def __str__(self):
        return str(self.amount)

    def time_in_mills(self):
        return int(self.time_stamp.timestamp()*1000)

    def get_month(self):
        return self.time_stamp.strftime("%m")

    def get_year(self):
        return self.time_stamp.strftime("%Y")

    def save(self, *args, **kwargs):
        if self.type == "welfare" and hasattr(self.user.profile, "welfare_contributor"):
            contributor = self.user.profile.welfare_contributor
            contributor.save()
        super(Transaction, self).save(*args, **kwargs)
