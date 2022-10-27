from datetime import datetime

from django.contrib.auth.models import AbstractUser, User
from django.db import models


# Create your models here.

class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    student_name = models.CharField(max_length=50, default="")
    student_email = models.CharField(max_length=50, default="")
    student_college = models.CharField(max_length=50, default="")
    student_cgpa = models.CharField(max_length=50, default="")
    student_resume = models.FileField(upload_to="media", default="")
    student_resume_result = models.CharField(max_length=50, default="")

    def __str__(self):
        return self.student_name
