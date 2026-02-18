"""
URL configuration for myapp project.

Topics 1-40: URL routing with static files
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', include('products.urls')),
]

# Topic 1-10: Serve static files in development
# Topic 16-17: Static file serving with DEBUG
if settings.DEBUG:
    # Topic 25-30: Serve media files in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
