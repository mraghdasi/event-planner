from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Avg
from django.utils import timezone


class Room(models.Model):
    title = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    capacity = models.IntegerField(default=0)
    description = models.TextField(null=True, blank=True, max_length=2000)

    def avg_rate(self):
        avg_rating = self.comments.aggregate(avg_rating=Avg('rate'))['avg_rating']
        if avg_rating:
            avg_rating = round(avg_rating)
            return avg_rating
        else:
            return 0

    def get_fill_star_range(self):
        return range(self.avg_rate())

    def get_gray_star_range(self):
        return range((5 - self.avg_rate()))

    def __str__(self):
        return f'{self.title} | {self.is_active}'


class Meeting(models.Model):
    title = models.CharField(max_length=255)
    team = models.ForeignKey('users.Team', related_name='meetings', on_delete=models.CASCADE)
    room = models.ForeignKey('meetings.Room', related_name='meetings', on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def get_status(self):
        now = timezone.now()
        if now >= self.end_date:
            return 'Passed'
        else:
            if now >= self.start_date:
                return 'Ongoing'
            else:
                return 'Reserved'

    def __str__(self):
        return f'{self.id} | {self.title} | {self.team.title} | {self.room.title}'


class CommentRoom(models.Model):
    user = models.ForeignKey(get_user_model(), related_name='comments', on_delete=models.CASCADE)
    room = models.ForeignKey('meetings.Room', related_name='comments', on_delete=models.CASCADE)
    body = models.TextField()
    rate = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    date = models.DateTimeField(auto_now_add=True)

    def get_fill_star_range(self):
        return range(self.rate)

    def get_gray_star_range(self):
        return range((5 - self.rate))

    def __str__(self):
        return f'{self.room.title} | {self.user.username} | {self.rate}'
