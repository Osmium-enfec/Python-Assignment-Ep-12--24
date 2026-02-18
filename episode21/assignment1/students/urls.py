from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('', views.student_list, name='list'),
    path('add/', views.add_student, name='add'),  # Topic 69: URL Routing for Forms
    path('<int:student_id>/edit/', views.edit_student, name='edit'),
    path('<int:student_id>/delete/', views.delete_student, name='delete'),
]
