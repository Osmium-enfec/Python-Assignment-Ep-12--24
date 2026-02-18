"""
URL routing for accounts app.

Topics 1-40: Auth views and URL patterns
"""
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

# TODO: Create app_name = 'accounts'

# TODO: Create urlpatterns with following paths (Topics 1-40):
# - path('register/', views.register, name='register') (Topic 1-2, 28-35)
# - path('login/', auth_views.LoginView.as_view(...), name='login') (Topic 3-5, 36-38)
# - path('logout/', auth_views.LogoutView.as_view(), name='logout') (Topic 6)
# - path('dashboard/', views.dashboard, name='dashboard') (Topic 7-9, 39-40)
# - path('profile/edit/', views.edit_profile, name='edit_profile') (Topic 11-20)
# - path('password/change/', auth_views.PasswordChangeView.as_view(...), name='password_change')
# - path('password/reset/', auth_views.PasswordResetView.as_view(...), name='password_reset')
# - path('verify/<str:code>/', views.verify_email, name='verify_email') (Topic 26-27)
