from django.db import models
from django.contrib.auth.models import User
import os
from datetime import date

def contact_photo_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{instance.first_name}_{instance.last_name}_{instance.id}.{ext}"
    return os.path.join('contact_photos', filename)

class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=20)
    address = models.TextField(blank=True, null=True)
    company = models.CharField(max_length=100, blank=True, null=True)
    job_title = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to=contact_photo_path, blank=True, null=True)
    is_favorite = models.BooleanField(default=False)
    birthday = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def days_until_birthday(self):
        if not self.birthday:
            return None
        today = date.today()
        next_birthday = self.birthday.replace(year=today.year)
        if next_birthday < today:
            next_birthday = next_birthday.replace(year=today.year + 1)
        return (next_birthday - today).days

    class Meta:
        ordering = ['first_name', 'last_name']