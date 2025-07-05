from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User 
# Create your models here.\


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile')
    nama_lengkap = models.CharField(blank=True,null=True,max_length = 255)
    nik = models.CharField(blank=True,null=True,max_length = 17)
    kk = models.CharField(blank=True,null=True,max_length=17)
    verified_identities = models.CharField(blank=True,null=True,max_length=255)
    token = models.CharField(blank=True,null=True,max_length=300)
    def __str__(self):
        return f"{self.user.username}', NIK: {self.nik} dan token:{self.token}"

# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_profile(sender,instance, **kwargs):
#     instance.profile.save()
