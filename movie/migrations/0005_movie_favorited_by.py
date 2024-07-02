# Generated by Django 4.2.13 on 2024-06-21 04:42

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movie', '0004_rename_user_customuser_alter_favoritemovie_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='favorited_by',
            field=models.ManyToManyField(blank=True, related_name='favorite_movies', to=settings.AUTH_USER_MODEL),
        ),
    ]
