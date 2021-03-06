from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length = 30)
    description = models.TextField(max_length = 2000)
    

class Recipe(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null = True)
    category_id = models.ForeignKey(Category, on_delete=models.SET_NULL, null = True)
    name = models.CharField(max_length = 30)
    description = models.TextField(max_length = 2000)
    ingredients = models.TextField(max_length = 2000)
    recipe_steps = models.TextField(max_length = 2000)
    image_file = models.FileField(upload_to='images/', null=True, verbose_name="")

class Comment(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null = True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    rating = models.FloatField(null=True)