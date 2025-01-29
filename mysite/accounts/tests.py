from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import UserProfile

class AccountsTests(TestCase):
    def test_user_registration(self):
        user = User.objects.create_user(username='testuser', password='superpuperpass123')
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_profile_creation(self):
        user = User.objects.create_user(username='testuser', password='superpuperpass123')
        profile = UserProfile.objects.create(user=user)
        self.assertTrue(UserProfile.objects.filter(user=user).exists())

    def test_profile_update(self):
        user = User.objects.create_user(username='testuser', password='superpuperpass123')
        profile = UserProfile.objects.create(user=user)
        profile.gender = 'male'
        profile.save()
        updated_profile = UserProfile.objects.get(user=user)
        self.assertEqual(updated_profile.gender, 'male')