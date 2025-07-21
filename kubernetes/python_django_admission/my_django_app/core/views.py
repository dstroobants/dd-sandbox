from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Task, Category, Profile
import json
import logging

logger = logging.getLogger(__name__)


def home(request):
    """Home page view."""
    return render(request, 'core/home.html', {
        'title': 'Welcome to Django App',
        'message': 'This is a simple Django boilerplate application!'
    })


def health_check(request):
    """Health check endpoint for Kubernetes."""
    return JsonResponse({
        'status': 'healthy',
        'service': 'django-app',
        'version': '1.0.0'
    })


def api_info(request):
    """API information endpoint."""
    return JsonResponse({
        'api_version': 'v1',
        'endpoints': {
            'health': '/health/',
            'tasks': '/api/tasks/',
            'categories': '/api/categories/'
        },
        'documentation': '/admin/'
    })


def task_list(request):
    """List all tasks with pagination and search."""
    search_query = request.GET.get('q', '')
    tasks = Task.objects.all()
    
    if search_query:
        tasks = tasks.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    paginator = Paginator(tasks, 10)  # Show 10 tasks per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'core/task_list.html', {
        'page_obj': page_obj,
        'search_query': search_query
    })


def task_detail(request, task_id):
    """Task detail view."""
    task = get_object_or_404(Task, id=task_id)
    return render(request, 'core/task_detail.html', {'task': task})


@login_required
def create_task(request):
    """Create a new task."""
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        
        if title:
            task = Task.objects.create(
                title=title,
                description=description,
                created_by=request.user
            )
            messages.success(request, f'Task "{task.title}" created successfully!')
            return redirect('task_detail', task_id=task.id)
        else:
            messages.error(request, 'Title is required!')
    
    return render(request, 'core/create_task.html')


# API Views
def api_tasks(request):
    """REST API endpoint for tasks."""
    if request.method == 'GET':
        tasks = Task.objects.all()
        data = []
        for task in tasks:
            data.append({
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'completed': task.completed,
                'created_by': task.created_by.username,
                'created_at': task.created_at.isoformat(),
                'updated_at': task.updated_at.isoformat()
            })
        return JsonResponse({'tasks': data})
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            # In a real app, you'd want proper authentication here
            task = Task.objects.create(
                title=data.get('title'),
                description=data.get('description', ''),
                created_by_id=1  # Placeholder - should be request.user.id
            )
            return JsonResponse({
                'id': task.id,
                'title': task.title,
                'status': 'created'
            }, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            logger.error(f'Error creating task: {e}')
            return JsonResponse({'error': 'Server error'}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


def api_categories(request):
    """REST API endpoint for categories."""
    if request.method == 'GET':
        categories = Category.objects.all()
        data = []
        for category in categories:
            data.append({
                'id': category.id,
                'name': category.name,
                'description': category.description,
                'color': category.color,
                'created_at': category.created_at.isoformat()
            })
        return JsonResponse({'categories': data})
    
    return JsonResponse({'error': 'Method not allowed'}, status=405) 
