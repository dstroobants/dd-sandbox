from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import User, BlogPost
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json


def hello_html(request):
    """Hello world view with HTML template"""
    context = {
        'title': 'Hello World',
        'message': 'Welcome to Django 4.2.24 with PostgreSQL!',
        'django_version': '4.2.24'
    }
    return render(request, 'hello/hello.html', context)


def psycopg2_demo(request):
    """Demonstrate PostgreSQL operations with psycopg2"""
    message = ""
    
    # Handle POST request for creating new users
    if request.method == 'POST':
        try:
            name = request.POST.get('name', '').strip()
            email = request.POST.get('email', '').strip()
            age = request.POST.get('age', '').strip()
            
            if name and email and age:
                user = User.objects.create(
                    name=name,
                    email=email,
                    age=int(age)
                )
                message = f"✅ Successfully created user: {user.name}"
            else:
                message = "❌ Please fill in all fields"
        except ValueError:
            message = "❌ Age must be a valid number"
        except Exception as e:
            message = f"❌ Error creating user: {str(e)}"
    
    try:
        # Create some sample users if they don't exist (only on first visit)
        user_count = User.objects.count()
            
        if user_count == 0:
            users_data = [
                {'name': 'Alice', 'email': 'alice@example.com', 'age': 25},
                {'name': 'Bob', 'email': 'bob@example.com', 'age': 30},
                {'name': 'Charlie', 'email': 'charlie@example.com', 'age': 28},
            ]
            for user_data in users_data:
                User.objects.create(**user_data)
        
        # Create sample blog posts if they don't exist
        post_count = BlogPost.objects.count()
            
        if post_count == 0:
            posts_data = [
                {
                    'title': 'Getting Started with PostgreSQL',
                    'content': 'PostgreSQL is a powerful relational database...',
                    'author': 'Alice',
                    'tags': ['postgresql', 'database', 'sql'],
                    'metadata': {'views': 100, 'likes': 15}
                },
                {
                    'title': 'Django with psycopg2',
                    'content': 'Using Django with PostgreSQL is straightforward with psycopg2...',
                    'author': 'Bob',
                    'tags': ['django', 'python', 'postgresql'],
                    'metadata': {'views': 250, 'likes': 32}
                }
            ]
            for post_data in posts_data:
                # Create the post with JSON data converted to strings
                post = BlogPost.objects.create(
                    title=post_data['title'],
                    content=post_data['content'],
                    author=post_data['author'],
                    tags=json.dumps(post_data['tags']),
                    metadata=json.dumps(post_data['metadata'])
                )
        
        # Get all users and posts
        users = User.objects.all()
        posts = BlogPost.objects.all()
        user_count = User.objects.count()
        post_count = BlogPost.objects.count()
        
        context = {
            'title': 'PostgreSQL Demo',
            'users': users,
            'posts': posts,
            'user_count': user_count,
            'post_count': post_count,
            'connection_status': 'Connected to PostgreSQL!',
            'message': message
        }
        
        return render(request, 'hello/psycopg2_demo.html', context)
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        context = {
            'title': 'PostgreSQL Demo',
            'error': f'Database connection error: {str(e)}',
            'error_details': error_details,
            'connection_status': 'Failed to connect to PostgreSQL'
        }
        return render(request, 'hello/psycopg2_demo.html', context)


@csrf_exempt
def api_users(request):
    """Simple API endpoint for users"""
    try:
        if request.method == 'GET':
            users = User.objects.all()
            users_data = []
            for user in users:
                users_data.append({
                    'id': user.id,
                    'name': user.name,
                    'email': user.email,
                    'age': user.age,
                    'created_at': user.created_at.isoformat() if user.created_at else None
                })
            return JsonResponse({'users': users_data})
        
        elif request.method == 'POST':
            data = json.loads(request.body)
            user = User.objects.create(
                name=data['name'],
                email=data['email'],
                age=data['age']
            )
            return JsonResponse({
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'age': user.age,
                'message': 'User created successfully!'
            })
            
    except Exception as e:
        import traceback
        return JsonResponse({
            'error': str(e),
            'traceback': traceback.format_exc()
        }, status=500)
