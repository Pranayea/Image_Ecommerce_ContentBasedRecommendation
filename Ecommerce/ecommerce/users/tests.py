from django.test import TestCase,SimpleTestCase
from django.urls import reverse,resolve
from django.contrib.auth.models import User
from .models import Profile
from datetime import datetime
from . import views
from django.contrib.auth import views as auth_views 
# Create your tests here.

class TestUserUrls(SimpleTestCase):

    def test_login_url_is_resolved(self):
        url = reverse("users:login")
        self.assertEqual(resolve(url).func.view_class,auth_views.LoginView)

    def test_register_url_is_resolved(self):
        url = reverse("users:register")
        self.assertEqual(resolve(url).func,views.registration)

    def test_logout_url_is_resolved(self):
        url = reverse("users:logout")
        self.assertEqual(resolve(url).func.view_class,auth_views.LogoutView)

    def test_profile_url_is_resolved(self):
        url = reverse("users:profile")
        self.assertEqual(resolve(url).func,views.user_profile)


class TestUsers(TestCase):

    def setUp(self):
        #creating instances of objects in User
       self.user1 = User.objects.create(username="PmPranaya",email="Pmpranaya@gmail.com")
       self.user2 = User.objects.create(username="PrmsPranaya",email="Prmspranaya@gmail.com")

    def test_users_is_created(self):
        #testing data in databases
        user1 = User.objects.get(username="PmPranaya")
        self.assertEqual(user1.username,"PmPranaya")
        self.assertEqual(user1.email,"Pmpranaya@gmail.com")

        user2 = User.objects.get(username="PrmsPranaya")
        self.assertEqual(user2.username,"PrmsPranaya")
        self.assertEqual(user2.email,"Prmspranaya@gmail.com")

