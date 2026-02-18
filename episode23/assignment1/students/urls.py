from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_student, name='add'),
    path('view/<int:student_id>/', views.view_student, name='view'),
    path('edit/<int:student_id>/', views.edit_student, name='edit'),
    path('delete/<int:student_id>/', views.delete_student, name='delete'),
]
