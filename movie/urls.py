# urls.py

from django.urls import path

from . import views
from .views import register, login_view, home_view, note, add

urlpatterns = [

    path('', views.login_view, name='login'),
    path('search/', views.search, name='search'),
    path('register/', views.register, name='register'),
    path('home/', views.home_view, name='home'),
    path('add/', views.add, name='add'),

    path('note/', views.note, name='note'),
    # path('favorite/', views.favorite, name='favorite'),
    # path('favorite/', views.favorite_list, name='favorite'),
    path('api/movie-details/', views.get_movie_details, name='movie-details'),
    path('search/', views.search, name='search'),
    path('profile/', views.profile, name='profile'),
    path('home/', views.review, name='home'),
    path('review/<int:id>/', views.review_page, name='review_page'),
    path('home/favorite/', views.favorite, name='favorite'),
    path('favorites/', views.favorite_list, name='favorite_list'),
    path('delete/<int:movie_id>/',views.delete,name='delete'),
    path('edit/<int:movie_id>/', views.edit, name='edit'),

]