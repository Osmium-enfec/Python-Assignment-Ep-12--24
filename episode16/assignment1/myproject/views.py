"""
EPISODE 16 - ASSIGNMENT 1: DJANGO VIEWS - STARTER CODE

This file contains the view functions for your first Django application.
Complete the TODO sections to create working views.

A view is a Python function that receives a web request and returns a response.
"""

from django.http import HttpResponse

# TODO 1: Create a 'welcome' view
# - Function name: welcome
# - Parameter: request (the HTTP request object)
# - Returns: HttpResponse with HTML content
# - Content should display: "Welcome to Django!" title and description
# Example:
#   return HttpResponse("<h1>Welcome to Django!</h1><p>This is my first Django view.</p>")

def welcome(request):
    """Display welcome page at root URL '/'"""
    # WRITE YOUR CODE HERE
    pass


# TODO 2: Create an 'about' view
# - Function name: about
# - Parameter: request
# - Returns: HttpResponse with HTML content
# - Content should display: "About Page" with some information about you
# Example:
#   return HttpResponse("<h1>About</h1><p>Learn more about Django...</p>")

def about(request):
    """Display about page at '/about/' URL"""
    # WRITE YOUR CODE HERE
    pass


# HINT: To test your views, you also need to update urls.py
# In myproject/urls.py, add these imports and URL patterns:
#
#   from myproject.views import welcome, about
#
#   urlpatterns = [
#       path('', welcome, name='welcome'),
#       path('about/', about, name='about'),
#       path('admin/', admin.site.urls),
#   ]
