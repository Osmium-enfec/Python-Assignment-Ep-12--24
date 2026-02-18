from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('add/', views.add_course, name='add_course'),
    path('<int:course_id>/edit/', views.edit_course, name='edit_course'),
    path('<int:course_id>/delete/', views.delete_course, name='delete_course'),
    path('validate/', views.validate_course, name='validate_course'),
]
