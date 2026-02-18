"""
URL routing for products app.

Topics 1-40: URL patterns for product views
"""
from django.urls import path
from . import views

# Topic 1-5: Define URL patterns
# TODO: Create app_name = 'products'
# TODO: Create urlpatterns with following paths (Topics 1-40):
# - path('', views.product_list, name='list') (Topic 1-2)
# - path('<int:product_id>/', views.product_detail, name='detail') (Topic 3-4)
# - path('<int:product_id>/image/', views.product_image, name='image') (Topic 36-37)
# - path('category/<str:category>/', views.product_by_category, name='by_category') (Topic 5)
# - path('upload/', views.product_upload, name='upload') (Topic 37)
# - path('uploaded/', views.uploaded_products, name='uploaded') (Topic 37)
