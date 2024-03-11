from django.contrib.messages import get_messages
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from meetings.models import Meeting, Room
from .models import User, Team


class UserAndTeamTests(TestCase):
    def setUp(self):
        # Create 2 teams
        self.team1 = Team.objects.create(title='Team 1', is_active=True)
        self.team2 = Team.objects.create(title='Team 2', is_active=True)

        # Create 10 users
        self.users = []
        for i in range(10):
            if i < 4:
                user = User.objects.create(username=f"user{i}", phone_number=f'123456789{i}', team=self.team1)
            elif 4 <= i < 7:
                user = User.objects.create(username=f"user{i}", phone_number=f'123456789{i}', team=self.team2)
            else:
                user = User.objects.create(username=f"user{i}", phone_number=f'123456789{i}')
            self.users.append(user)
        self.users.append(
            User.objects.create(username='user10', phone_number='1234567811', team=self.team1, is_lead=True))
        self.users.append(
            User.objects.create(username='user11', phone_number='1234567812', team=self.team2, is_lead=True))

    def test_user_and_team_creation(self):
        # Check if 10 users and 2 teams are created
        self.assertEqual(User.objects.count(), 12)
        self.assertEqual(Team.objects.count(), 2)

    def test_read_users_and_teams(self):
        # Read users and teams
        users = User.objects.all()
        teams = Team.objects.all()

        # Check if they are read correctly
        self.assertEqual(len(users), 12)
        self.assertEqual(len(teams), 2)

    def test_update_user_team(self):
        # Remove one user from team 1 and add one user to team 2
        user_to_move = User.objects.filter(team=self.team1).first()
        user_to_move.team = self.team2
        user_to_move.save()

        # Check if the user is removed from team 1 and added to team 2
        self.assertEqual(User.objects.filter(team=self.team1).count(), 4)
        self.assertEqual(User.objects.filter(team=self.team2).count(), 5)

    def test_str_methods(self):
        # Check the __str__ method for users and teams
        for user in self.users:
            self.assertEqual(str(user), f'{user.username} | {user.get_full_name()}')
        self.assertEqual(str(self.team1),
                         f'{self.team1.title}')
        self.assertEqual(str(self.team2),
                         f'{self.team2.title}')

    def test_delete_user_team(self):
        # Test the on delete method
        self.team1.delete()
        self.assertEqual(User.objects.filter(team__isnull=True).count(), 8)
        self.assertEqual(User.objects.filter(team__isnull=False).count(), 4)

    def test_get_lead(self):
        # Test for reading team leads
        self.assertEqual(User.objects.filter(is_lead=True).count(), 2)

    def test_get_leads_by_team(self):
        # Test getting team leads for each team
        self.assertEqual(User.objects.get(is_lead=True, team=self.team1).username, 'user10')
        self.assertEqual(User.objects.get(is_lead=True, team=self.team2).username, 'user11')


class UserViewsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', email='test@example.com', password='testpassword',
                                             first_name='test', last_name='test', phone_number='09195449241')
        self.client = Client()

    def test_profile_view_authenticated(self):
        self.client.login(username='test_user', password='testpassword')

        response = self.client.get(reverse('profile'))

        self.assertEqual(response.status_code, 200)

    def test_profile_view_unauthenticated(self):
        response = self.client.get(reverse('profile'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/users/sign_in/?next=/users/profile/')

    def test_sign_up_view(self):
        response = self.client.get(reverse('sign_up'))
        self.assertEqual(response.status_code, 200)

    def test_sign_in_view(self):
        response = self.client.get(reverse('sign_in'))

        self.assertEqual(response.status_code, 200)

    def test_sign_out_view(self):
        self.client.login(username='test_user', password='testpassword')

        response = self.client.get(reverse('sign_out'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/users/sign_in/')

    def test_sign_in_otp_view(self):
        response = self.client.post(reverse('sign_in_otp'))

        self.assertEqual(response.status_code, 200)

    def test_sign_in_otp_confirmation_view(self):
        self.client.session['phone_number'] = '09195449242'
        self.client.session['otp'] = '1234'

        response = self.client.post(reverse('sign_in_otp_confirmation'), {'otp': '1234'})

        self.assertEqual(response.status_code, 302)


class ProfileViewTestCase(TestCase):
    def setUp(self):
        self.team = Team.objects.create(title='test_team')
        self.user = User.objects.create_user(username='test_user', email='test@example.com', password='testpassword',
                                             first_name='test', last_name='test', phone_number='09195449242',
                                             team=self.team)
        self.room = Room.objects.create(title='test_room', capacity=10)
        self.client = Client()
        self.meeting = Meeting.objects.create(title='test_meeting', team=self.team, room=self.room,
                                              start_date=timezone.now(),
                                              end_date=timezone.now())

    def test_profile_view_get(self):
        self.client.login(username='test_user', password='testpassword')

        response = self.client.get(reverse('profile'))

        self.assertEqual(response.status_code, 200)

    def test_profile_view_post_valid_form(self):
        self.client.login(username='test_user', password='testpassword')

        response = self.client.post(reverse('profile'),
                                    {'username': 'test_user',
                                     'email': 'test@example.com',
                                     'first_name': 'Updated',
                                     'last_name': 'User',
                                     'phone_number': '09195449241'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.get(username='test_user').first_name, 'Updated')
        self.assertEqual(User.objects.get(username='test_user').last_name, 'User')

    def test_profile_view_messages(self):
        self.client.login(username='test_user', password='testpassword')

        response = self.client.post(reverse('profile'),
                                    {'username': 'test_user',
                                     'email': 'test@example.com',
                                     'first_name': 'Updated',
                                     'last_name': 'User',
                                     'phone_number': '09195449241'})

        storage = get_messages(response.wsgi_request)
        messages = list(storage)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'User Updated Successfully!')

    def test_profile_view_meetings(self):
        self.client.login(username='test_user', password='testpassword')

        response = self.client.get(reverse('profile'))

        self.assertEqual(response.context['meetings'].count(), 1)
