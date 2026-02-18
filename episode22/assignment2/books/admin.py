from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'price', 'genre', 'is_published')
    list_filter = ('is_published', 'genre')
    search_fields = ('title', 'author', 'isbn')
