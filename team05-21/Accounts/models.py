from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class MyUser(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    is_email_verified = models.BooleanField(null=True)
    course_id = models.ForeignKey('Profile.Course', null=True, on_delete=models.SET_NULL)
    year_of_study = models.PositiveIntegerField(null=True)

    def __str__(self):
        return self.username
