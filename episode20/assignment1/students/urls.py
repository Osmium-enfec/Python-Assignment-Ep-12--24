from django.urls import path
from . import views

# Topic 7: app_name - Namespace for this app's URLs
app_name = 'students'

# Topic 8: URL Patterns List - All routes for students app
urlpatterns = [
    # Topic 1: URL Routing - Basic path mapping
    # Topic 2: path() Function - Django function for URL definition
    # Topic 6: URL Name - Named URL patterns for reversal
    path('', views.student_list, name='list'),
    
    # Topic 3: URL Parameters - <int:student_id> captures integer from URL
    # Topic 4: int Converter - Converts string to integer, ensures only digits match
    path('<int:student_id>/', views.student_detail, name='detail'),
    
    # Topic 5: str Converter - <str:roll_no> captures string values
    path('roll/<str:roll_no>/', views.view_student_info, name='by_roll'),
    
    # URL for filtering by GPA
    # float converter in Django requires custom implementation or str converter
    path('gpa/<str:min_gpa>/', views.student_by_gpa, name='by_gpa'),
    
    # Create student
    path('create/', views.create_student, name='create'),
    
    # Edit student
    path('<int:student_id>/edit/', views.edit_student, name='edit'),
    
    # Delete student
    path('<int:student_id>/delete/', views.delete_student, name='delete'),
    
    # Search
    path('search/', views.search_students, name='search'),
    
    # Export as JSON
    path('<int:student_id>/export/', views.export_student_data, name='export'),
    
    # Redirect example
    path('redirect-list/', views.redirect_to_list, name='redirect_list'),
]
