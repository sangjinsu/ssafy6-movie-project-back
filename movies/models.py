from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.


class Genre(models.Model):
    name = models.CharField(max_length=50)


class Movie(models.Model):
    title = models.CharField(max_length=100)
    release_date = models.DateField()
    popularity = models.FloatField()
    vote_count = models.IntegerField()
    vote_average = models.FloatField()
    overview = models.TextField()
    poster_path = models.CharField(max_length=200)
    genres = models.ManyToManyField(Genre, related_name='movies')
    original_title = models.CharField(max_length=100)
    like_users = models.ManyToManyField(
        get_user_model(), related_name='like_movies')
    pick_users = models.ManyToManyField(
        get_user_model(), related_name='pick_movies')
