from datetime import timezone

from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User

from movielast import settings


class CustomUser(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])

    def __str__(self):
        return self.username


# models.py


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=500)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=241)
    release_date = models.DateField()
    actors = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    trailer_link = models.URLField()
    image = models.ImageField(upload_to='movie_images/')
    favorited_by = models.ManyToManyField(User, related_name='favorite_movies', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='movies')  # New field


def __str__(self):
    return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_images', default='default.jpg')
    mobile = models.CharField(max_length=15, blank=True, null=True)
    address1 = models.CharField(max_length=255, blank=True, null=True)
    address2 = models.CharField(max_length=255, blank=True, null=True)
    postcode = models.CharField(max_length=10, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    area = models.CharField(max_length=50, blank=True, null=True)
    education = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    region = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'


class review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Movie, on_delete=models.CASCADE)
    review_desp = models.CharField(max_length=100)
    rating = models.IntegerField()

    def __str__(self):
        return f'{self.user.username} - {self.item.title}'


class FavoriteMovie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'movie')

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"
