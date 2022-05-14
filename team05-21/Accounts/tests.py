# Create your tests here.
from django.contrib.auth import get_user_model
from django.test import TestCase


# https://testdriven.io/blog/django-custom-user-model/#project-setup
class UsersManagersTests(TestCase):

    def test_create_user(self):
        user = get_user_model()
        newUser = user.objects.create_user(email='normal@user.com', password='foo')
        self.assertEqual(newUser.email, 'normal@user.com')
        self.assertTrue(newUser.is_active)
        self.assertFalse(newUser.is_staff)
        self.assertFalse(newUser.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(newUser.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            user.objects.create_user()
        with self.assertRaises(TypeError):
            user.objects.create_user(email='')
        with self.assertRaises(ValueError):
            user.objects.create_user(email='', password="foo")

    def test_create_superuser(self):
        user = get_user_model()
        adminUser = user.objects.create_superuser(email='super@user.com', password='foo')
        self.assertEqual(adminUser.email, 'super@user.com')
        self.assertTrue(adminUser.is_active)
        self.assertTrue(adminUser.is_staff)
        self.assertTrue(adminUser.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(adminUser.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            user.objects.create_superuser(
                email='super@user.com', password='foo', is_superuser=False)