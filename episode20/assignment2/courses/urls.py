from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.course_list, name='list'),
    path('api/<int:course_id>/detail/', views.course_detail_ajax, name='detail_ajax'),
    path('api/<int:course_id>/edit-form/', views.course_edit_form, name='edit_form'),
    path('api/<int:course_id>/update/', views.update_course_ajax, name='update'),
    path('api/<int:course_id>/enrollments/', views.course_enrollments, name='enrollments'),
    path('api/<int:course_id>/enroll/', views.enroll_student, name='enroll'),
    path('api/<int:course_id>/delete-confirm/', views.delete_course_confirm, name='delete_confirm'),
    path('api/<int:course_id>/delete/', views.delete_course, name='delete'),
    path('api/stats/', views.course_stats, name='stats'),
    path('api/search/', views.search_courses, name='search'),
]
