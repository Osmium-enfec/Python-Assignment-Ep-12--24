from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('', views.book_list, name='list'),
    path('create/', views.book_create, name='create'),
    path('<int:book_id>/edit/', views.book_update, name='update'),
    path('<int:book_id>/delete/', views.book_delete, name='delete'),
]
