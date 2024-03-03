from django.contrib.auth.models import User
from django.test import TestCase
from .models import Profile, Team


class ProfileAndTeamTests(TestCase):
    def setUp(self):
        # Create 2 teams
        self.team1 = Team.objects.create(title='Team 1', is_active=True)
        self.team2 = Team.objects.create(title='Team 2', is_active=True)

        # Create 10 users
        self.users = []
        for i in range(10):
            if i < 4:
                user = Profile.objects.create(username=f"user{i}", phone_number='1234567890', team=self.team1, role='u')
            elif 4 <= i < 7:
                user = Profile.objects.create(username=f"user{i}", phone_number='1234567890', team=self.team2, role='u')
            else:
                user = Profile.objects.create(username=f"user{i}", phone_number='1234567890', role='u')
            self.users.append(user)
        self.users.append(
            Profile.objects.create(username='user10', phone_number='1234567890', team=self.team1, role='l'))
        self.users.append(
            Profile.objects.create(username='user11', phone_number='1234567890', team=self.team2, role='l'))

    def test_user_and_team_creation(self):
        # Check if 10 users and 2 teams are created
        self.assertEqual(Profile.objects.count(), 12)
        self.assertEqual(Team.objects.count(), 2)

    def test_read_users_and_teams(self):
        # Read users and teams
        users = Profile.objects.all()
        teams = Team.objects.all()

        # Check if they are read correctly
        self.assertEqual(len(users), 12)
        self.assertEqual(len(teams), 2)

    def test_update_user_team(self):
        # Remove one user from team 1 and add one user to team 2
        user_to_move = Profile.objects.filter(team=self.team1).first()
        user_to_move.team = self.team2
        user_to_move.save()

        # Check if the user is removed from team 1 and added to team 2
        self.assertEqual(Profile.objects.filter(team=self.team1).count(), 4)
        self.assertEqual(Profile.objects.filter(team=self.team2).count(), 5)

    def test_str_methods(self):
        # Check the __str__ method for users and teams
        for user in self.users:
            self.assertEqual(str(user), f'{user.username} | {user.get_full_name()}')
        self.assertEqual(str(self.team1),
                         f'{self.team1.title} | {Profile.objects.filter(team=self.team1.id).count()} | {self.team1.is_active}')
        self.assertEqual(str(self.team2),
                         f'{self.team2.title} | {Profile.objects.filter(team=self.team2.id).count()} | {self.team2.is_active}')

    def test_delete_user_team(self):
        # Test the on delete method
        self.team1.delete()
        self.assertEqual(Profile.objects.filter(team__isnull=True).count(), 8)
        self.assertEqual(Profile.objects.filter(team__isnull=False).count(), 4)

    def test_get_lead(self):
        # Test for reading team leads
        self.assertEqual(Profile.objects.filter(role='l').count(), 2)

    def test_get_leads_by_team(self):
        # Test getting team leads for each team
        self.assertEqual(Profile.objects.get(role='l', team=self.team1).username, 'user10')
        self.assertEqual(Profile.objects.get(role='l', team=self.team2).username, 'user11')
