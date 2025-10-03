"""
Views demonstrating PyMongo (sync), Motor (async), and Celery usage
"""
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from datetime import datetime
from bson import ObjectId
import asyncio

from .db import get_mongo_db, get_motor_db
from .models import create_user_document, create_blog_post_document, serialize_document
from .tasks import add_numbers, process_user_data, generate_report


def index(request):
    """Main page with links to all demos"""
    context = {
        'title': 'Django + PyMongo + Motor + Celery Demo',
        'message': 'Explore the different features using the links below'
    }
    return render(request, 'hello/index.html', context)


def hello_html(request):
    """Simple hello world view"""
    context = {
        'title': 'Hello World',
        'message': 'Welcome to Django 5.2.6 with PyMongo, Motor, and Celery!',
        'django_version': '5.2.6'
    }
    return render(request, 'hello/hello.html', context)


def mongodb_sync_demo(request):
    """Demonstrate synchronous MongoDB operations with PyMongo"""
    db = get_mongo_db()
    message = ""
    
    # Handle POST request for creating new users
    if request.method == 'POST':
        try:
            name = request.POST.get('name', '').strip()
            email = request.POST.get('email', '').strip()
            age = request.POST.get('age', '').strip()
            
            if name and email and age:
                user_doc = create_user_document(name, email, int(age))
                result = db.users.insert_one(user_doc)
                message = f"✅ Successfully created user: {name} (ID: {result.inserted_id})"
            else:
                message = "❌ Please fill in all fields"
        except ValueError:
            message = "❌ Age must be a valid number"
        except Exception as e:
            message = f"❌ Error creating user: {str(e)}"
    
    try:
        # Create sample data if collections are empty
        user_count = db.users.count_documents({})
        if user_count == 0:
            sample_users = [
                create_user_document('Alice', 'alice@example.com', 25),
                create_user_document('Bob', 'bob@example.com', 30),
                create_user_document('Charlie', 'charlie@example.com', 28),
            ]
            db.users.insert_many(sample_users)
        
        post_count = db.blog_posts.count_documents({})
        if post_count == 0:
            sample_posts = [
                create_blog_post_document(
                    'Getting Started with MongoDB',
                    'MongoDB is a great NoSQL database that provides flexibility and scalability...',
                    'Alice',
                    tags=['mongodb', 'database', 'nosql'],
                    metadata={'views': 100, 'likes': 15}
                ),
                create_blog_post_document(
                    'Django with PyMongo and Motor',
                    'Using Django with MongoDB through PyMongo and Motor gives you both sync and async capabilities...',
                    'Bob',
                    tags=['django', 'python', 'mongodb', 'motor'],
                    metadata={'views': 250, 'likes': 32}
                ),
                create_blog_post_document(
                    'Background Tasks with Celery',
                    'Celery is a powerful distributed task queue that helps you run background jobs...',
                    'Charlie',
                    tags=['celery', 'python', 'tasks'],
                    metadata={'views': 180, 'likes': 24}
                )
            ]
            db.blog_posts.insert_many(sample_posts)
        
        # Fetch all users and posts
        users = list(db.users.find().limit(50))
        posts = list(db.blog_posts.find().limit(50))
        
        # Serialize documents for template
        users_serialized = [serialize_document(u) for u in users]
        posts_serialized = [serialize_document(p) for p in posts]
        
        context = {
            'title': 'PyMongo Sync Demo',
            'users': users_serialized,
            'posts': posts_serialized,
            'user_count': db.users.count_documents({}),
            'post_count': db.blog_posts.count_documents({}),
            'connection_status': 'Connected to MongoDB (PyMongo - Sync)',
            'message': message
        }
        
        return render(request, 'hello/mongodb_sync.html', context)
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        context = {
            'title': 'MongoDB Sync Demo',
            'error': f'Database connection error: {str(e)}',
            'error_details': error_details,
            'connection_status': 'Failed to connect to MongoDB'
        }
        return render(request, 'hello/mongodb_sync.html', context)


def mongodb_async_demo(request):
    """
    Demonstrate Motor's async capabilities.
    Note: Since Django views are sync by default and Motor requires an async context,
    we'll demonstrate Motor's features using PyMongo for this simple demo.
    
    In a real async Django app (using async def views), you would use Motor directly.
    For now, we'll show the same data but highlight that this would be async with Motor.
    """
    # Use PyMongo for compatibility with sync Django views
    db = get_mongo_db()
    
    try:
        # Ensure sample data exists
        user_count = db.users.count_documents({})
        if user_count == 0:
            sample_users = [
                create_user_document('David', 'david@example.com', 35),
                create_user_document('Eve', 'eve@example.com', 29),
            ]
            db.users.insert_many(sample_users)
        
        # Fetch data (in a real async view with Motor, these would be: await db.users.find()...)
        users = list(db.users.find().limit(50))
        posts = list(db.blog_posts.find().limit(50))
        
        user_count = db.users.count_documents({})
        post_count = db.blog_posts.count_documents({})
        
        # Serialize documents for template
        users_serialized = [serialize_document(u) for u in users]
        posts_serialized = [serialize_document(p) for p in posts]
        
        context = {
            'title': 'Motor Async Demo',
            'users': users_serialized,
            'posts': posts_serialized,
            'user_count': user_count,
            'post_count': post_count,
            'connection_status': 'Connected to MongoDB (Motor-style operations)',
            'note': 'This demo shows the data structure. In an async Django view (async def), Motor would provide true non-blocking I/O.'
        }
        
        return render(request, 'hello/mongodb_async.html', context)
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        context = {
            'title': 'Motor Async Demo',
            'error': f'Database connection error: {str(e)}',
            'error_details': error_details,
            'connection_status': 'Failed to connect to MongoDB'
        }
        return render(request, 'hello/mongodb_async.html', context)


def celery_demo(request):
    """Demonstrate Celery task execution"""
    task_results = []
    
    if request.method == 'POST':
        task_type = request.POST.get('task_type')
        
        if task_type == 'add':
            x = int(request.POST.get('x', 5))
            y = int(request.POST.get('y', 10))
            task = add_numbers.delay(x, y)
            task_results.append({
                'task_id': task.id,
                'task_name': 'Add Numbers',
                'status': 'Processing...',
                'description': f'Adding {x} + {y}'
            })
        
        elif task_type == 'report':
            task = generate_report.delay()
            task_results.append({
                'task_id': task.id,
                'task_name': 'Generate Report',
                'status': 'Processing...',
                'description': 'Generating daily report'
            })
    
    context = {
        'title': 'Celery Tasks Demo',
        'task_results': task_results
    }
    
    return render(request, 'hello/celery_demo.html', context)


# API Endpoints

@csrf_exempt
@require_http_methods(["GET", "POST"])
def api_users(request):
    """REST API endpoint for users (PyMongo)"""
    db = get_mongo_db()
    
    try:
        if request.method == 'GET':
            users = list(db.users.find().limit(100))
            users_data = [serialize_document(u) for u in users]
            return JsonResponse({'users': users_data, 'count': len(users_data)})
        
        elif request.method == 'POST':
            data = json.loads(request.body)
            user_doc = create_user_document(
                data['name'],
                data['email'],
                int(data['age'])
            )
            result = db.users.insert_one(user_doc)
            user_doc['_id'] = result.inserted_id
            
            return JsonResponse({
                'message': 'User created successfully!',
                'user': serialize_document(user_doc)
            }, status=201)
            
    except Exception as e:
        import traceback
        return JsonResponse({
            'error': str(e),
            'traceback': traceback.format_exc()
        }, status=500)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def api_posts(request):
    """REST API endpoint for blog posts (PyMongo)"""
    db = get_mongo_db()
    
    try:
        if request.method == 'GET':
            posts = list(db.blog_posts.find().limit(100))
            posts_data = [serialize_document(p) for p in posts]
            return JsonResponse({'posts': posts_data, 'count': len(posts_data)})
        
        elif request.method == 'POST':
            data = json.loads(request.body)
            post_doc = create_blog_post_document(
                data['title'],
                data['content'],
                data['author'],
                tags=data.get('tags', []),
                metadata=data.get('metadata', {})
            )
            result = db.blog_posts.insert_one(post_doc)
            post_doc['_id'] = result.inserted_id
            
            return JsonResponse({
                'message': 'Blog post created successfully!',
                'post': serialize_document(post_doc)
            }, status=201)
            
    except Exception as e:
        import traceback
        return JsonResponse({
            'error': str(e),
            'traceback': traceback.format_exc()
        }, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def api_task_status(request, task_id):
    """Check the status of a Celery task"""
    from celery.result import AsyncResult
    
    task = AsyncResult(task_id)
    
    response_data = {
        'task_id': task_id,
        'status': task.state,
        'ready': task.ready(),
    }
    
    if task.ready():
        if task.successful():
            response_data['result'] = task.result
        else:
            response_data['error'] = str(task.info)
    
    return JsonResponse(response_data)


@csrf_exempt
@require_http_methods(["POST"])
def api_trigger_task(request):
    """Trigger a Celery task via API"""
    try:
        data = json.loads(request.body)
        task_type = data.get('task_type')
        
        if task_type == 'add':
            x = data.get('x', 5)
            y = data.get('y', 10)
            task = add_numbers.delay(x, y)
            
        elif task_type == 'report':
            report_type = data.get('report_type', 'daily')
            task = generate_report.delay(report_type)
            
        elif task_type == 'process_user':
            user_id = data.get('user_id')
            if not user_id:
                return JsonResponse({'error': 'user_id is required'}, status=400)
            task = process_user_data.delay(user_id)
            
        else:
            return JsonResponse({'error': 'Invalid task_type'}, status=400)
        
        return JsonResponse({
            'message': 'Task submitted successfully',
            'task_id': task.id,
            'task_type': task_type
        }, status=202)
        
    except Exception as e:
        import traceback
        return JsonResponse({
            'error': str(e),
            'traceback': traceback.format_exc()
        }, status=500)
