from django.test import TestCase
from django.contrib.auth import get_user_model

# Create your tests here.

class UsersManagersTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='norma', email='normal@user.com', password='foo', first_name='Norma',
            last_name='Smith', address='Rudy Dr, San Jose, CA', phone='4089995959')
        self.assertEqual(user.email, 'normal@user.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email='')
        # with self.assertRaises(ValueError):
        #    User.objects.create_user(username='zorana',
        #        email='', password="foo", first_name='Norma', last_name='Smith',
        #        address='San Jose, CA', phone='408')
"""
    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser('super', 'foo', 'super@yahoo.com', 'Sup', 'Per', 'Street, Town, ZIP', '3339093333')
        self.assertEqual(admin_user.username, 'super')
        # self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                username='super', password='foo', email='super@yahoo.com',
                first_name='Sup', last_name='Per', address='St', phone='408',
                is_superuser=False)

"""
