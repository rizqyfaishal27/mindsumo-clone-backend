from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from tinymce.models import HTMLField

from .managers import CustomUserManager

# Create your models here.

PRIVACY_SETTINGS = [
    (1, "Public to everyone"),
    (2, "Private to you and companies")
]

CHALENGE_STATUS = [
    (1, "Available"),
    (2, "On process review"),
    (3, "Closed")
]

class Skill(models.Model):
    skill_name = models.CharField(max_length=150)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.skill_name

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, null=False)
    email = models.CharField(max_length=255, unique=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    username = models.CharField(max_length=150, null=False,unique=True)
    birthdate = models.DateField(null=True, blank=True)
    hometown = models.CharField(null=True, max_length=255, blank=True)
    phone_number = models.CharField(null=True, max_length=15, blank=True)
    facebook_id = models.CharField(max_length=255, null=True, blank=True)
    twitter_id = models.CharField(max_length=255, null=True, blank=True)
    skills = models.ManyToManyField(Skill)
    activities_and_interest = HTMLField(blank=True)
    organization_team_clubs = HTMLField(blank=True)
    privacy_setting = models.IntegerField(choices=PRIVACY_SETTINGS, default=1)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'first_name',
        'last_name',
        'username'
    ]

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class Challenge(models.Model):
    title = models.CharField(max_length=255, null=False)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    skills = models.ManyToManyField(Skill)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateField(null=False)
    description = HTMLField()
    deliverables = HTMLField()
    status = models.IntegerField(choices=CHALENGE_STATUS, null=False)
    banner_image = models.ImageField(upload_to="challenges/", blank=False, null=False)
    is_anonymous_author = models.BooleanField(default=False)

    def __str__(self):
        return self.title



class Submission(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    submission_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    submission_title = models.CharField(max_length=100)
    submission_text = HTMLField()
    submission_file = models.FileField(upload_to="files/", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.challenge) + ' ' + self.submission_title

# class AttachmentFile(models.Model):
#     submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
#     file = models.FileField(upload_to="files/")
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

