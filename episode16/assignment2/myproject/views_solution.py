"""
EPISODE 16 - ASSIGNMENT 2: MULTIPLE VIEWS - SOLUTION

This file contains the complete solutions for Assignment 2 views.
Refer to this file if you get stuck on your implementation.
"""

from django.http import HttpResponse, JsonResponse


def home(request):
    """
    Display home page at root URL '/'
    Main landing page with links to all sections
    
    Returns:
        HttpResponse: HTML page with navigation
    """
    html_content = """
    <html>
        <head>
            <title>Home</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 50px; }
                h1 { color: #092E20; }
                p { font-size: 16px; }
                a { 
                    display: inline-block;
                    padding: 10px 20px;
                    margin: 5px;
                    background-color: #092E20;
                    color: white;
                    text-decoration: none;
                    border-radius: 5px;
                }
                a:hover { background-color: #0f4d28; }
            </style>
        </head>
        <body>
            <h1>Welcome to My Blog Platform</h1>
            <p>Explore our amazing content and services.</p>
            
            <h2>Navigation</h2>
            <div>
                <a href="/">🏠 Home</a>
                <a href="/blog/">📝 Blog</a>
                <a href="/contact/">📧 Contact</a>
                <a href="/api/data/">🔌 API Data</a>
            </div>
        </body>
    </html>
    """
    return HttpResponse(html_content)


def blog_list(request):
    """
    Display list of all blog posts at '/blog/'
    
    Returns:
        HttpResponse: HTML page showing blog posts
    """
    html_content = """
    <html>
        <head>
            <title>Blog</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 50px; }
                h1 { color: #092E20; }
                .post { 
                    border: 1px solid #ddd;
                    padding: 15px;
                    margin: 10px 0;
                    border-radius: 5px;
                }
                a { color: #092E20; text-decoration: none; }
                a:hover { text-decoration: underline; }
                .back { display: inline-block; margin: 20px 0; }
            </style>
        </head>
        <body>
            <h1>Blog Posts</h1>
            
            <div class="post">
                <h3><a href="/blog/1/">Django Basics</a></h3>
                <p>Learn the fundamentals of Django web framework.</p>
                <small>Posted on 2024-01-15</small>
            </div>
            
            <div class="post">
                <h3><a href="/blog/2/">Building APIs with Django</a></h3>
                <p>Create RESTful APIs using Django Rest Framework.</p>
                <small>Posted on 2024-02-10</small>
            </div>
            
            <div class="post">
                <h3><a href="/blog/3/">Database Optimization</a></h3>
                <p>Tips and tricks for optimizing Django databases.</p>
                <small>Posted on 2024-02-15</small>
            </div>
            
            <div class="back">
                <a href="/">← Back to Home</a>
            </div>
        </body>
    </html>
    """
    return HttpResponse(html_content)


def blog_detail(request, post_id):
    """
    Display details of a specific blog post at '/blog/<post_id>/'
    
    Args:
        request: HTTP request object
        post_id: ID of the blog post to display
    
    Returns:
        HttpResponse: HTML page showing blog post details
    """
    # Sample blog posts data
    posts = {
        1: {
            'title': 'Django Basics',
            'author': 'John Developer',
            'date': '2024-01-15',
            'content': 'Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. It handles much of the complexity of web development, so you can focus on writing your app without needing to reinvent the wheel.'
        },
        2: {
            'title': 'Building APIs with Django',
            'author': 'Jane Developer',
            'date': '2024-02-10',
            'content': 'Django Rest Framework (DRF) is a powerful and flexible toolkit for building REST APIs. It provides serializers for easy data serialization, viewsets for API views, and routers for URL configuration.'
        },
        3: {
            'title': 'Database Optimization',
            'author': 'Bob Developer',
            'date': '2024-02-15',
            'content': 'Database performance is crucial for web applications. Learn about query optimization, indexing, database connection pooling, and caching strategies to improve your application performance.'
        }
    }
    
    # Get post or show error
    if post_id not in posts:
        return HttpResponse(f"<h1>Post #{post_id} not found</h1><p><a href='/blog/'>← Back to Blog</a></p>", status=404)
    
    post = posts[post_id]
    
    html_content = f"""
    <html>
        <head>
            <title>{post['title']}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 50px; max-width: 800px; }}
                h1 {{ color: #092E20; }}
                .meta {{ color: #666; margin: 10px 0; }}
                .content {{ line-height: 1.6; }}
                a {{ color: #092E20; text-decoration: none; }}
                a:hover {{ text-decoration: underline; }}
            </style>
        </head>
        <body>
            <h1>{post['title']}</h1>
            <div class="meta">
                <strong>Author:</strong> {post['author']}<br>
                <strong>Published:</strong> {post['date']}<br>
            </div>
            <div class="content">
                <p>{post['content']}</p>
            </div>
            <hr>
            <p><a href="/blog/">← Back to Blog</a> | <a href="/">Home</a></p>
        </body>
    </html>
    """
    return HttpResponse(html_content)


def contact(request):
    """
    Display contact form page at '/contact/'
    
    Returns:
        HttpResponse: HTML page with contact form
    """
    html_content = """
    <html>
        <head>
            <title>Contact</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 50px; }
                h1 { color: #092E20; }
                form { max-width: 400px; }
                label { display: block; margin-top: 10px; font-weight: bold; }
                input, textarea { 
                    width: 100%;
                    padding: 8px;
                    margin-top: 5px;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    box-sizing: border-box;
                }
                button { 
                    margin-top: 15px;
                    padding: 10px 20px;
                    background-color: #092E20;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                }
                button:hover { background-color: #0f4d28; }
                a { color: #092E20; text-decoration: none; }
            </style>
        </head>
        <body>
            <h1>Contact Us</h1>
            <p>Have a question? We'd love to hear from you!</p>
            
            <form method="POST">
                <label for="name">Name:</label>
                <input type="text" id="name" name="name" required>
                
                <label for="email">Email:</label>
                <input type="email" id="email" name="email" required>
                
                <label for="message">Message:</label>
                <textarea id="message" name="message" rows="5" required></textarea>
                
                <button type="submit">Send Message</button>
            </form>
            
            <p><a href="/">← Back to Home</a></p>
        </body>
    </html>
    """
    return HttpResponse(html_content)


def api_response(request):
    """
    Return JSON data at '/api/data/'
    
    Returns:
        JsonResponse: JSON data with blog statistics
    """
    data = {
        'status': 'success',
        'message': 'API endpoint working correctly',
        'data': {
            'total_posts': 3,
            'total_authors': 3,
            'latest_post': {
                'id': 3,
                'title': 'Database Optimization',
                'date': '2024-02-15'
            }
        },
        'endpoints': {
            'home': '/',
            'blog_list': '/blog/',
            'blog_detail': '/blog/<id>/',
            'contact': '/contact/',
            'api': '/api/data/'
        }
    }
    return JsonResponse(data)
