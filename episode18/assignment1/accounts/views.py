"""
Views for user authentication and account management.

Topics 1-40: Login, register, profile management
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .models import UserProfile
from .forms import UserRegistrationForm, UserUpdateForm, UserProfileForm
import secrets

# TODO: Implement views (Topics 1-40)

# def register(request):
#     """
#     Topic 1-2, 28-35: User registration view
#     - Handle GET: display registration form (Topic 1-2)
#     - Handle POST: validate and create user (Topic 28-30)
#     - Topic 33: Check password strength
#     - Topic 34: Check email uniqueness
#     - Topic 35: Create UserProfile with verification code
#     - Redirect to login after success
#     """
#     pass

# def dashboard(request):
#     """
#     Topic 7-9, 39-40: User dashboard
#     - Topic 7: Require authentication with @login_required
#     - Topic 8: Display user info
#     - Topic 9: Display profile info
#     - Topic 39-40: Show user activity or stats
#     """
#     pass

# @login_required(login_url='accounts:login')
# def edit_profile(request):
#     """
#     Topic 11-20: Edit user profile
#     - Handle GET: display profile form (Topic 11-12)
#     - Handle POST: validate and save changes (Topic 14-20)
#     - Topic 15: Handle avatar upload
#     - Topic 16: Save date of birth
#     - Topic 23: Check profile completeness
#     """
#     pass

# def verify_email(request, code):
#     """
#     Topic 26-27: Email verification
#     - Topic 26: Get verification code from URL
#     - Topic 27: Find UserProfile by code
#     - Mark is_verified = True
#     - Redirect to dashboard
#     """
#     pass

# def password_change_success(request):
#     """Topic 25: Redirect after password change"""
#     messages.success(request, 'Password changed successfully!')
#     return redirect('accounts:dashboard')
