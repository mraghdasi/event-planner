from django.contrib.auth.models import AbstractUser
from django.db import models
from image_optimizer.fields import OptimizedImageField


class User(AbstractUser):
    image = OptimizedImageField(upload_to='User', optimized_image_output_size=(32, 32),
                                optimized_image_resize_method='cover', null=True, blank=True)
    phone_number = models.CharField(max_length=11)
    team = models.ForeignKey('account.Team', related_name='members', on_delete=models.SET_NULL, null=True, blank=True)
    is_lead = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.username} | {self.get_full_name()}'


class Team(models.Model):
    title = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.title} | {self.members.all().count()} | {self.is_active}'
