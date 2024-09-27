from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import uuid 

#model for users
class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=255, blank=True, default="")
    phone_number = models.CharField(max_length=15, blank=True, default="")
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, default="")

    def __str__(self):
        return self.username 

#model for booking
class Service(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Booking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    user_email = models.EmailField(default="")
    queue_number = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"{self.user.username} - {self.service.name} at {self.date_time}"


