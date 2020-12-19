from django.test import SimpleTestCase
from django.urls import reverse 
from CookIT.views import index
from django.test.client import RequestFactory
from http.cookies import SimpleCookie

class HomePageTest(SimpleTestCase):
   def test_home_page(self):
      response = self.client.get('/CookIT/')
      self.assertEqual(response.status_code, 200)
      self.assertTemplateUsed(response, 'base.html')
      self.assertContains(response, 'Hello')

class AccountPageTest(SimpleTestCase):
   def test_user_with_cookie(self):
      self.client.cookies = SimpleCookie({'userSession': 'testCookie'})
      response = self.client.get('/CookIT/account/')
      self.assertEqual(response.status_code, 200)
      self.assertTemplateUsed(response, 'base.html')
      self.assertContains(response, 'Account')

   def test_user_without_cookie(self):
      self.client.cookies = SimpleCookie({})
      response = self.client.get('/CookIT/account/')
      self.assertEqual(response.status_code, 302)
      self.assertEqual(response.url, '/CookIT/login')