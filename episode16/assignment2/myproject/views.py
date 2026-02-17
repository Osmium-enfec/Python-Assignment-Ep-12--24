"""
EPISODE 16 - ASSIGNMENT 2: MULTIPLE VIEWS - STARTER CODE

This file contains the view function templates for your Django application.
Complete the TODO sections to create working views.

A view is a Python function that receives a web request and returns a response.
"""

from django.http import HttpResponse, JsonResponse

# TODO 1: Create a 'home' view
# - Function name: home
# - Parameter: request
# - Returns: HttpResponse with HTML content
# - Show a landing page with links to blog, contact, and API endpoints
# Hint: Use <a href="..."> tags for navigation links

def home(request):
    """Display home page at root URL '/'"""
    # WRITE YOUR CODE HERE
    pass


# TODO 2: Create a 'blog_list' view
# - Function name: blog_list
# - Parameter: request
# - Returns: HttpResponse with HTML content
# - Display a list of blog posts with links to each post
# - Each post should have a title and link to /blog/<id>/
# Hint: Create at least 3 sample blog posts

def blog_list(request):
    """Display list of blog posts at '/blog/'"""
    # WRITE YOUR CODE HERE
    pass


# TODO 3: Create a 'blog_detail' view
# - Function name: blog_detail
# - Parameters: request, post_id
# - Returns: HttpResponse with HTML content
# - Display details of a specific blog post
# - Use the post_id parameter to get the correct post
# - Return 404 if post_id doesn't exist
# Hint: Create a dictionary with sample posts, use post_id to look up data

def blog_detail(request, post_id):
    """Display details of a blog post at '/blog/<post_id>/'"""
    # WRITE YOUR CODE HERE
    pass


# TODO 4: Create a 'contact' view
# - Function name: contact
# - Parameter: request
# - Returns: HttpResponse with HTML form
# - Display a contact form with fields: name, email, message
# - Form should have submit button
# Hint: Use HTML <form>, <input>, <textarea> elements

def contact(request):
    """Display contact form at '/contact/'"""
    # WRITE YOUR CODE HERE
    pass


# TODO 5: Create an 'api_response' view
# - Function name: api_response
# - Parameter: request
# - Returns: JsonResponse with JSON data
# - Return data about blog statistics or any useful information
# - Use JsonResponse instead of HttpResponse
# Hint: Create a dictionary and pass it to JsonResponse()

def api_response(request):
    """Return JSON response at '/api/data/'"""
    # WRITE YOUR CODE HERE
    pass


# HINT: To make these views work, update urls.py with:
#
#   from myproject.views import home, blog_list, blog_detail, contact, api_response
#
#   urlpatterns = [
#       path('', home, name='home'),
#       path('blog/', blog_list, name='blog_list'),
#       path('blog/<int:post_id>/', blog_detail, name='blog_detail'),
#       path('contact/', contact, name='contact'),
#       path('api/data/', api_response, name='api_response'),
#       path('admin/', admin.site.urls),
#   ]
