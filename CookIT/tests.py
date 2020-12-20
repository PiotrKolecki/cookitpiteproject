from django.test import SimpleTestCase
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.urls import reverse 
from CookIT.views import index
from CookIT.models import Category, Recipe, Comment
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

class CategoryTest(TestCase):
    def setUp(self):
        self.category = Category(name="Test name")
        self.category.description = "Test description"
        self.category.save()
        
    def test_create_category(self):
        new_category = Category.objects.get(name="Test name")
        self.assertEqual(new_category.name, "Test name")
        self.assertEqual(new_category.description, "Test description")
        
class RecipeTest(TestCase):
    def setUp(self):
        self.recipe = Recipe(name="Test name")
        self.recipe.description = "Test description"
        self.recipe.ingredients = "Test ingredients"
        self.recipe.recipe_steps = "Test recipe steps"
        self.recipe.save()
        
    def test_create_recipe(self):
        new_recipe = Recipe.objects.get(name="Test name")
        self.assertEqual(new_recipe.name, "Test name")
        self.assertEqual(new_recipe.description, "Test description")
        self.assertEqual(new_recipe.ingredients, "Test ingredients")
        self.assertEqual(new_recipe.recipe_steps, "Test recipe steps")
        
        
class CommentTest(TestCase):
    def setUp(self):
        self.recipe = Recipe(name="Test name")
        self.recipe.save()
        
        self.comment = Comment(recipe = self.recipe)       
        self.comment.text = "Comment test"
        self.comment.rating = 5.0
        self.comment.save()
        
    def test_create_comment(self):
        comment_list = Comment.objects.filter(recipe = self.recipe)
        self.assertEqual(comment_list[0].recipe.name, "Test name")
        self.assertEqual(comment_list[0].text, "Comment test")
        self.assertEqual(comment_list[0].rating, 5.0)
        
    def test_cascade_delete(self):
        comment_list = Comment.objects.filter(recipe = self.recipe)     
        self.recipe.delete()
        self.assertEqual(len(comment_list),0)
        
class ValidationTest(TestCase):
    def test_category_max_length(self):
        long_name = "x" * 31   
        self.category = Category(name = long_name)  
        self.assertRaises(ValidationError,  self.category.full_clean)
        
    def test_recipe_max_length(self):
        long_name = "x" * 31
        self.recipe = Recipe(name = long_name)
        self.assertRaises(ValidationError,  self.recipe.full_clean)
        
    def test_comment_rating_type(self):
        self.recipe = Recipe(name="test")
        self.comment = Comment(recipe = self.recipe, rating = "bad type")
        self.assertRaises(ValidationError,  self.comment.full_clean)
        
      
        