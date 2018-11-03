from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Skill(models.Model):
    skill_name = models.CharField(max_length=150)

