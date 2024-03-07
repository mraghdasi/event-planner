from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Room(models.Model):
    title = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.title} | {self.is_active}'


class Meeting(models.Model):
    title = models.CharField(max_length=255)
    team = models.ForeignKey('users.Team', related_name='meetings', on_delete=models.CASCADE)
    room = models.ForeignKey('meetings.Room', related_name='meetings', on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return f'{self.id} | {self.title} | {self.team.title} | {self.room.title}'


class CommentRoom(models.Model):
    user = models.ForeignKey(get_user_model(), related_name='comments', on_delete=models.CASCADE)
    room = models.ForeignKey('meetings.Room', related_name='comments', on_delete=models.CASCADE)
    body = models.TextField()
    rate = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return f'{self.room.title} | {self.user.username} | {self.rate}'
