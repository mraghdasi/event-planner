from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from users.models import Team, User
from meetings.models import Room, Meeting
from datetime import datetime, timedelta
from admin_dash.forms import EditUserForm, TeamForm, RoomForm, MeetingForm


class ViewsTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
        self.team = Team.objects.create(title='Test Team', is_active=True)
        self.room = Room.objects.create(title='Test Room', is_active=True, capacity=10, description='Test description')
        self.meeting = Meeting.objects.create(
            title='Test Meeting',
            team=self.team,
            room=self.room,
            start_date=datetime.now() + timedelta(days=1),
            end_date=datetime.now() + timedelta(days=2)
        )

    def test_admin_home_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('admin_home'))
        self.assertEqual(response.status_code, 302)

    def test_admin_users_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('admin_users'))
        self.assertEqual(response.status_code, 302)

    def test_admin_meetings_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('admin_meetings'))
        self.assertEqual(response.status_code, 302)

    def test_admin_rooms_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('admin_rooms'))
        self.assertEqual(response.status_code, 302)

    def test_admin_teams_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('admin_teams'))
        self.assertEqual(response.status_code, 302)

    def test_edit_user_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('edit_user', args=[self.user.pk]))
        self.assertEqual(response.status_code, 302)

    def test_edit_team_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('edit_team', args=[self.team.pk]))
        self.assertEqual(response.status_code, 302)

    def test_add_team_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('add_team'))
        self.assertEqual(response.status_code, 302)

    def test_edit_room_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('edit_room', args=[self.room.pk]))
        self.assertEqual(response.status_code, 302)

    def test_add_room_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('add_room'))
        self.assertEqual(response.status_code, 302)

    def test_edit_meeting_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('edit_meeting', args=[self.meeting.pk]))
        self.assertEqual(response.status_code, 302)

    def test_delete_meeting_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('delete_meeting', args=[self.meeting.pk]))
        self.assertEqual(response.status_code, 302)


class FormsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.team = Team.objects.create(title='Test Team', is_active=True)
        self.room = Room.objects.create(title='Test Room', is_active=True)
        self.meeting = Meeting.objects.create(
            title='Test Meeting',
            team=self.team,
            room=self.room,
            start_date='2024-03-07 22:30:00',
            end_date='2024-03-07 23:30:00'
        )



    def test_edit_user_form_invalid_data(self):
        form_data = {
            'username': '',
            'email': 'invalidemail',
            'first_name': '',
            'last_name': '',
            'phone_number': 'invalidphone',
            'image': 'invalidpath',
            'is_lead': 'notbool',
            'team': 'invalidteam',
        }
        form = EditUserForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_team_form_valid_data(self):
        form_data = {
            'title': 'New Team',
            'is_active': True,
        }
        form = TeamForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_team_form_invalid_data(self):
        form_data = {
            'title': '',
            'is_active': 'notbool',
        }
        form = TeamForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_room_form_valid_data(self):
        form_data = {
            'title': 'New Room',
            'capacity': 100,
            'description': 'salam chetori',
            'is_active': True,
        }
        form = RoomForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_room_form_invalid_data(self):
        form_data = {
            'title': '',
            'is_active': 'notbool',
        }
        form = RoomForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_meeting_form_valid_data(self):
        form_data = {
            'title': 'New Meeting',
            'team': self.team.pk,
            'room': self.room.pk,
            'start_date': '2024-03-20 12:00:00',  # Write this based on current date
            'end_date': '2024-03-21 14:00:00',
        }
        form = MeetingForm(data=form_data)
        self.assertTrue(form.is_valid())

