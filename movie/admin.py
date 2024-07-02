from django.contrib import admin
from .models import Category, Movie, FavoriteMovie, Profile, review, CustomUser


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description','slug')
    search_fields = ('name',)


admin.site.register(Category, CategoryAdmin)


admin.site.register(Movie)


admin.site.register(FavoriteMovie)

admin.site.register(CustomUser)


admin.site.register(Profile)

admin.site.register(review)

