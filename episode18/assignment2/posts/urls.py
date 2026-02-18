"""
URL routing for posts app.

Topics 41-80: Post views with permission checking
"""
from django.urls import path
from . import views

# TODO: Create app_name = 'posts'

# TODO: Create urlpatterns with following paths (Topics 41-80):
# - path('', views.post_list, name='list') (Topic 41-50)
# - path('<int:post_id>/', views.post_detail, name='detail') (Topic 51-70)
# - path('create/', views.post_create, name='create') (Topic 71-75)
# - path('<int:post_id>/edit/', views.post_edit, name='edit') (Topic 76-80)
# - path('<int:post_id>/delete/', views.post_delete, name='delete') (Topic 76-80)
# - path('<int:post_id>/approve/', views.approve_comment, name='approve_comment')
# - path('login/', auth_views.LoginView.as_view(...), name='login')
# - path('logout/', auth_views.LogoutView.as_view(), name='logout')
