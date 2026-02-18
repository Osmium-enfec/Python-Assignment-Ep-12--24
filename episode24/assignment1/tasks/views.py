from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Task
from .forms import TaskForm

def task_list(request):
    """
    Display all tasks ordered by priority and creation date
    """
    tasks = Task.objects.all()
    return render(request, 'task_list.html', {'tasks': tasks})

def task_create(request):
    """
    Create a new task - GET displays form, POST saves new task
    """
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task created successfully!')
            return redirect('tasks:list')
    else:
        form = TaskForm()
    return render(request, 'task_form.html', {'form': form, 'action': 'Create'})

def task_detail(request, task_id):
    """
    Display task details using get_object_or_404 for safety
    """
    task = get_object_or_404(Task, pk=task_id)
    return render(request, 'task_detail.html', {'task': task})

def task_update(request, task_id):
    """
    Update task - GET displays form with instance data, POST saves changes
    """
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('tasks:detail', task_id=task.id)
    else:
        form = TaskForm(instance=task)
    return render(request, 'task_form.html', {'form': form, 'action': 'Update', 'task': task})

def task_delete(request, task_id):
    """
    Delete task - GET displays confirmation, POST deletes task
    """
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully!')
        return redirect('tasks:list')
    return render(request, 'task_confirm_delete.html', {'task': task})
