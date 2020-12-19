from django.test import SimpleTestCase
from django.test import TestCase
from django.urls import reverse 
from CookIT.views import index
from django.test.client import RequestFactory
from http.cookies import SimpleCookie
from django.test import Client
from django.contrib.auth.models import User

class HomePageTest(SimpleTestCase):
   def test_home_page(self):
      response = self.client.get('/CookIT/')
      self.assertEqual(response.status_code, 200)
      self.assertTemplateUsed(response, 'base.html')
      self.assertContains(response, 'Hello')

class AccountPageTest(SimpleTestCase):
   def test_user_without_cookie(self):
      self.client.cookies = SimpleCookie({})
      response = self.client.get('/CookIT/account/')
      self.assertEqual(response.status_code, 302)
      self.assertEqual(response.url, '/CookIT/login')

class AccountPageTestAuthenticated(TestCase):
   def test_user_with_cookie(self):
      self.client.cookies = SimpleCookie({'userSession': 'testCookie'})
      user = User.objects.create_user(username="test", password="test")
      user.save()
      self.client.login(username='test', password='test')
      response = self.client.get('/CookIT/account/')
      self.assertEqual(response.status_code, 200)
      self.assertTemplateUsed(response, 'account.html')
      self.assertContains(response, 'Account')
