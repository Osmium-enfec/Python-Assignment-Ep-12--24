"""
URL routing for gallery app.

Topics 1-40: URL patterns for gallery views
"""
from django.urls import path
from . import views

# Topic 1-5: Define URL patterns
# TODO: Create app_name = 'gallery'
# TODO: Create urlpatterns with following paths (Topics 1-80):
# - path('', views.gallery_list, name='list') (Topic 1-2)
# - path('<int:gallery_id>/', views.gallery_detail, name='detail') (Topic 3-4)
# - path('image/<int:image_id>/', views.image_view, name='image_view') (Topic 36-40)
# - path('image/<int:image_id>/comments/', views.image_comments, name='image_comments') (Topic 61-70)
# - path('comment/<int:comment_id>/approve/', views.approve_comment, name='approve_comment') (Topic 68-70)
# - path('upload/', views.upload_images, name='upload') (Topic 37)
