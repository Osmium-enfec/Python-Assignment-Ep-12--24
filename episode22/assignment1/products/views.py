from django.shortcuts import render
from .models import Product

# Topic 23-29: Template Tags and Variables
def product_list(request):
    """
    Topic 24: {% if %} Tag - Conditional rendering
    Topic 25: {% for %} Tag - Looping sequences
    Display all products with proper template structure
    """
    products = Product.objects.all()
    context = {
        'products': products,
        'page_title': 'Product List',  # Topic 28: Template Variables
    }
    return render(request, 'products/list.html', context)

def product_detail(request, product_id):
    """
    Topic 28: Template Variables - Passing context
    Display individual product detail
    """
    product = Product.objects.get(id=product_id)
    context = {
        'product': product,
        'page_title': f'Product: {product.name}',
    }
    return render(request, 'products/detail.html', context)

def product_categories(request):
    """
    Topic 25: {% for %} Tag - Iterate over data
    Topic 31: |date Filter - Date formatting
    Display products by category
    """
    products = Product.objects.all()
    categories = products.values_list('category', flat=True).distinct()
    context = {
        'categories': categories,
        'products': products,
        'page_title': 'Product Categories',
    }
    return render(request, 'products/categories.html', context)
