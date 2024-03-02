from django.contrib.auth.models import User
from django.db import models
from image_optimizer.fields import OptimizedImageField


class Profile(User):
    image = OptimizedImageField(upload_to='Profile', optimized_image_output_size=(32, 32),
                                optimized_image_resize_method='cover', null=True, blank=True)
    phone_number = models.CharField(max_length=11)
    role = models.CharField(max_length=2, choices=(('a', 'admin'), ('u', 'user')))

    def __str__(self):
        return f'{self.username} | {self.get_full_name()}'


class Team(models.Model):
    title = models.CharField(max_length=255, unique=True)
    users = models.ManyToManyField('account.Profile', related_name='teams')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.title} | {self.users.count()} | {self.is_active}'
