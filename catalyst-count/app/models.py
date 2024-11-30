from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):
    uuid = models.BigIntegerField(null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    domain = models.CharField(max_length=255, null=True, blank=True)
    year_founded = models.IntegerField(null=True, blank=True)
    industry = models.CharField(max_length=255, null=True, blank=True)
    size_range = models.CharField(max_length=50, null=True, blank=True)
    locality = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    linkedin_url = models.URLField(max_length=500, null=True, blank=True)
    current_employee_estimate = models.IntegerField(null=True, blank=True)
    total_employee_estimate = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class UploadHistory(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="upload_histories"
    )
    file_name = models.CharField(max_length=255)
    progress = models.FloatField(default=0.0)
    status = models.CharField(max_length=255, default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_name
