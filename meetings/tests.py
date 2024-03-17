# tests.py

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

from users.models import Team
from .models import Room, Meeting, CommentRoom

from .forms import MeetingForm, CommentRoomForm
from datetime import datetime, timedelta


class MeetingModelTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
        self.team = Team.objects.create(title='Test Team')
        self.room = Room.objects.create(title='Test Room', is_active=True, capacity=10)
        self.meeting = Meeting.objects.create(title='Test Meeting', team=self.team, room=self.room,
                                              start_date=timezone.now(), end_date=timezone.now())

    def test_meeting_status(self):
        self.assertEqual(self.meeting.get_status(), 'Passed')  # Adjust as needed based on your logic


class RoomModelTestCase(TestCase):
    def setUp(self):
        self.room = Room.objects.create(title='Test Room', is_active=True, capacity=10)
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')

    def test_avg_rate_with_comments(self):
        CommentRoom.objects.create(user=self.user, room=self.room, body='Test Comment', rate=5)
        CommentRoom.objects.create(user=self.user, room=self.room, body='Another Comment', rate=3)

        expected_avg_rate = (5 + 3) / 2

        self.assertEqual(self.room.avg_rate(), expected_avg_rate)

    def test_avg_rate_without_comments(self):
        # Test the avg_rate function when there are no comments
        self.assertEqual(self.room.avg_rate(), 0)

    def test_get_fill_star_range(self):
        # Test the get_fill_star_range function with a specific rating
        comment = CommentRoom.objects.create(user=self.user, room=self.room, body='Test Comment', rate=4)
        self.assertEqual(list(comment.get_fill_star_range()), [1, 2, 3, 4])

    def test_get_gray_star_range(self):
        # Test the get_gray_star_range function with a specific rating
        comment = CommentRoom.objects.create(user=self.user, room=self.room, body='Test Comment', rate=2)
        self.assertEqual(list(comment.get_gray_star_range()), [3, 4, 5])


class CommentRoomModelTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
        self.room = Room.objects.create(title='Test Room', is_active=True, capacity=10)
        self.comment = CommentRoom.objects.create(user=self.user, room=self.room, body='Test Comment', rate=4)

    def test_get_fill_star_range(self):
        self.assertEqual(list(self.comment.get_fill_star_range()), [1, 2, 3, 4])

    def test_get_gray_star_range(self):
        self.assertEqual(list(self.comment.get_gray_star_range()), [5])


class RoomListViewTestCase(TestCase):
    def test_room_list_view(self):
        # Create a user and log in
        user = get_user_model().objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

        response = self.client.get(reverse('meeting:room_list'))
        self.assertEqual(response.status_code, 200)


class RoomDetailViewTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
        self.room = Room.objects.create(title='Test Room', is_active=True, capacity=10)

    def test_room_detail_view(self):
        response = self.client.get(reverse('meeting:room_detail', args=[self.room.id]))
        self.assertEqual(response.status_code, 200)


class CreateCommentViewTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
        self.room = Room.objects.create(title='Test Room', is_active=True, capacity=10)

    def test_create_comment_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('meeting:create_comment', args=[self.room.id]))
        self.assertEqual(response.status_code, 200)


class RoomCommentsViewTestCase(TestCase):
    def setUp(self):
        self.room = Room.objects.create(title='Test Room', is_active=True, capacity=10)

    def test_room_comments_view(self):
        # Create a user and log in
        user = get_user_model().objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

        response = self.client.get(reverse('meeting:room_comments', args=[self.room.id]))
        self.assertEqual(response.status_code, 200)


class FormsTestCase(TestCase):
    def setUp(self):
        self.team = Team.objects.create(title='Test Team', is_active=True)
        self.room = Room.objects.create(title='Test Room', is_active=True, capacity=10, description='Test description')
        self.meeting = Meeting.objects.create(
            title='Test Meeting',
            team=self.team,
            room=self.room,
            start_date=datetime.now() + timedelta(days=1),
            end_date=datetime.now() + timedelta(days=2)
        )


    def test_comment_room_form_valid_data(self):
        form_data = {
            'body': 'Test Comment',
            'rate': 4,
        }
        form = CommentRoomForm(data=form_data, user=get_user_model(), room=self.room)
        self.assertTrue(form.is_valid())

    def test_comment_room_form_invalid_data(self):
        form_data = {
            'body': '',
            'rate': 6,
        }
        form = CommentRoomForm(data=form_data, user=get_user_model(), room=self.room)
        self.assertFalse(form.is_valid())

    def test_comment_room_form_save(self):
        form_data = {
            'body': 'Test Comment',
            'rate': 4,
        }
        user = get_user_model().objects.create_user(username='testuser', password='testpass')
        form = CommentRoomForm(data=form_data, user=user, room=self.room)
        self.assertTrue(form.is_valid())

        comment = form.save()

        self.assertEqual(comment.user, user)
        self.assertEqual(comment.body, 'Test Comment')
        self.assertEqual(comment.rate, 4)
        self.assertEqual(comment.room, self.room)
