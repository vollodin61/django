from django.db import models
from django.contrib.auth.models import User


def profile_avatar_directory_path(instance: "Profile", filename: str) -> str:
    return 'profiles/profile_{pk}/avatar/{filename}'.format(
        pk=instance.pk,
        filename=filename,
    )


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=100, blank=True)
    agreement_accepted = models.BooleanField(default=False)
    avatar = models.ImageField(null=True, blank=True, upload_to=profile_avatar_directory_path)


def profile_image_directory_path(instance: "ProfileImage", filename: str) -> str:
    return 'profiles/profile_{pk}/images/{filename}'.format(
        pk=instance.profile.pk,
        filename=filename,
    )

class ProfileImage(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=profile_image_directory_path)
    description = models.CharField(max_length=200, null=True, blank=True)
