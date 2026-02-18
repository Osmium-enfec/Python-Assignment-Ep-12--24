"""
Forms for user authentication and registration.

Topics 1-40: Auth forms, user registration, login
"""
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import UserProfile

# TODO: Topic 1-10: Implement custom forms

# Topic 31: UserRegistrationForm extending UserCreationForm
# - Fields: username, email, password1, password2
# - Validation: check email uniqueness (Topic 32)
# - Help text: password requirements (Topic 33)

# Topic 1-5: LoginForm for email/username + password
# - Fields: username_or_email, password
# - Widget for password: PasswordInput (Topic 3)

# Topic 11-20: UserProfileForm for profile editing
# - Fields: bio, phone, avatar, date_of_birth
# - Widgets: Textarea for bio, DateInput for DOB

# Topic 6: UserUpdateForm for user details
# - Fields: first_name, last_name, email
# - Validation: email uniqueness check
