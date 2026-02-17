"""
EPISODE 16 - ASSIGNMENT 1: DJANGO VIEWS - SOLUTION

This file contains the complete solutions for Assignment 1 views.
Refer to this file if you get stuck on your implementation.
"""

from django.http import HttpResponse


def welcome(request):
    """
    Display welcome page at root URL '/'
    
    Returns:
        HttpResponse: HTML page with welcome message
    """
    html_content = """
    <html>
        <head>
            <title>Welcome to Django</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 50px; }
                h1 { color: #092E20; }
                p { font-size: 16px; }
                a { color: #092E20; text-decoration: none; margin-right: 20px; }
            </style>
        </head>
        <body>
            <h1>Welcome to Django!</h1>
            <p>This is my first Django application.</p>
            <p>Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design.</p>
            <p>
                <a href="/">Home</a>
                <a href="/about/">About</a>
            </p>
        </body>
    </html>
    """
    return HttpResponse(html_content)


def about(request):
    """
    Display about page at '/about/' URL
    
    Returns:
        HttpResponse: HTML page with about information
    """
    html_content = """
    <html>
        <head>
            <title>About</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 50px; }
                h1 { color: #092E20; }
                p { font-size: 16px; }
                a { color: #092E20; text-decoration: none; margin-right: 20px; }
            </style>
        </head>
        <body>
            <h1>About This Project</h1>
            <p>This is a Django learning project created for Episode 16.</p>
            <p><strong>Key Topics:</strong></p>
            <ul>
                <li>Django views and HTTP responses</li>
                <li>URL routing and patterns</li>
                <li>HTML rendering with Django</li>
                <li>Development server</li>
            </ul>
            <p>
                <a href="/">Home</a>
                <a href="/about/">About</a>
            </p>
        </body>
    </html>
    """
    return HttpResponse(html_content)
