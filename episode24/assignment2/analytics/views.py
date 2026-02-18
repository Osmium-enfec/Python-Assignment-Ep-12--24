from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count, Q, F, Avg
from .models import Project, Event, Analytics
from .forms import ProjectForm, EventForm

# Topic 56: Query optimization with select_related
def project_list(request):
    """
    List all projects with optimized queries
    Topic 56: Using select_related for one-to-one relationships
    """
    projects = Project.objects.select_related('analytics').all()
    return render(request, 'project_list.html', {'projects': projects})

# Topic 57: Query optimization with prefetch_related
def project_detail(request, project_id):
    """
    Project detail with optimized event queries
    Topic 57: Using prefetch_related for reverse relationships
    """
    project = get_object_or_404(Project.objects.select_related('analytics'), pk=project_id)
    events = project.events.all()[:100]  # Get last 100 events
    
    # Topic 63: Calculate statistics
    stats = {
        'total_events': events.count(),
        'event_types': Event.objects.filter(project=project).values('event_type').annotate(count=Count('id')),
    }
    
    return render(request, 'project_detail.html', {
        'project': project,
        'events': events,
        'stats': stats
    })

# Topic 58: Efficient aggregation
def analytics_dashboard(request):
    """
    Analytics dashboard with efficient aggregations
    Topic 58: Using aggregate() for calculations
    """
    projects = Project.objects.all()
    
    # Efficient aggregations
    total_stats = Event.objects.aggregate(
        total_events=Count('id'),
        total_views=Count('id', filter=Q(event_type='view')),
        total_clicks=Count('id', filter=Q(event_type='click')),
        total_errors=Count('id', filter=Q(event_type='error')),
        avg_duration=Avg('duration_ms'),
    )
    
    return render(request, 'analytics_dashboard.html', {
        'projects': projects,
        'total_stats': total_stats
    })

# Topic 59: Data update patterns
def project_create(request):
    """
    Create project and initialize analytics
    Topic 59: Creating related objects together
    """
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            # Topic 59: Create related analytics record
            Analytics.objects.create(project=project)
            messages.success(request, 'Project created successfully!')
            return redirect('analytics:project_detail', project_id=project.id)
    else:
        form = ProjectForm()
    return render(request, 'project_form.html', {'form': form, 'action': 'Create'})

def project_update(request, project_id):
    """
    Update project with safety
    Topic 64: PUT/POST for updates
    """
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project updated!')
            return redirect('analytics:project_detail', project_id=project.id)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'project_form.html', {'form': form, 'action': 'Update', 'project': project})

def event_create(request):
    """
    Create event with validation
    Topic 65: Event logging validation
    """
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save()
            messages.success(request, 'Event logged!')
            return redirect('analytics:project_detail', project_id=event.project.id)
    else:
        form = EventForm()
    return render(request, 'event_form.html', {'form': form})

# Topic 66: Bulk operations for performance
def event_bulk_create(request):
    """
    Bulk create events for testing
    Topic 66: Using bulk_create for efficiency
    """
    if request.method == 'POST':
        project_id = request.POST.get('project_id')
        project = get_object_or_404(Project, pk=project_id)
        
        # Topic 66: Bulk create events
        events = [
            Event(project=project, event_type='view', duration_ms=100),
            Event(project=project, event_type='click', duration_ms=50),
            Event(project=project, event_type='submit', duration_ms=200),
        ]
        Event.objects.bulk_create(events)
        messages.success(request, 'Events created!')
        return redirect('analytics:project_detail', project_id=project.id)
    
    projects = Project.objects.all()
    return render(request, 'event_bulk_form.html', {'projects': projects})
